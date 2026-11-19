#!/usr/bin/env python3
"""Validate canonical Skills, Codex plugin marketplace, paths and local links."""
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"engineering-docs-router", "technical-architecture-design", "module-detailed-design", "technical-implementation-documentation", "technical-document-review"}
errors = []
skills_dir = ROOT / "skills"
found = {}
for skill_file in skills_dir.glob("*/SKILL.md"):
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{skill_file}: missing YAML frontmatter"); continue
    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append(f"{skill_file}: malformed frontmatter"); continue
    header = parts[1]
    name = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", header)
    desc = re.search(r"(?m)^description:\s*(.+)$", header)
    if not name or not desc:
        errors.append(f"{skill_file}: frontmatter requires name and description"); continue
    if name.group(1) != skill_file.parent.name:
        errors.append(f"{skill_file}: name does not match directory")
    found[name.group(1)] = skill_file
if set(found) != EXPECTED:
    errors.append(f"Skill set mismatch: found={sorted(found)}")

plugin_root = ROOT / "plugins/codex"
try:
    manifest = json.loads((plugin_root / "plugin.json").read_text(encoding="utf-8"))
    if manifest.get("name") != "software-technical-docs-assistant":
        errors.append("Codex plugin name mismatch")
    if not (plugin_root / "skills").exists() or not (plugin_root / "skills/engineering-docs-router/SKILL.md").exists():
        errors.append("Codex plugin skills link is missing or broken")
except Exception as exc:
    errors.append(f"Invalid plugin manifest or skills link: {exc}")
try:
    market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    entries = market.get("plugins", [])
    if len(entries) != 1 or entries[0].get("source", {}).get("path") != "./plugins/codex":
        errors.append("Marketplace must expose ./plugins/codex")
except Exception as exc:
    errors.append(f"Invalid marketplace JSON: {exc}")

for rel in ["assets/templates/01_技术架构设计模板.md", "assets/templates/02_模块详细设计模板.md", "assets/templates/03_技术实现文档模板.md", "assets/templates/04_技术决策记录模板.md", "scripts/render_docx.py", "INSTALL.md", "CONTRIBUTING.md", "LICENSE"]:
    if not (ROOT / rel).exists():
        errors.append(f"Missing required path: {rel}")

for md in [ROOT/"README.md", ROOT/"README.zh-CN.md", ROOT/"INSTALL.md", ROOT/"CONTRIBUTING.md"]:
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", md.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "#", "mailto:")): continue
        if not (md.parent / target.split("#",1)[0]).resolve().exists():
            errors.append(f"{md.name}: broken local link {target}")

for f in ROOT.rglob("*"):
    if not f.is_file() or f.is_symlink(): continue
    try: content = f.read_text(encoding="utf-8")
    except UnicodeDecodeError: continue
    if re.search(r"(?i)(gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)", content):
        errors.append(f"Potential secret detected: {f.relative_to(ROOT)}")

if errors:
    print("VALIDATION FAILED"); print("\n".join(f"- {e}" for e in errors)); sys.exit(1)
print(f"PASS: {len(found)} Skills, manifests, marketplace, templates and local links")
