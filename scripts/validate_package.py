from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess
import sys
import tempfile

from build import NAMES, PLUGIN, RESOURCES, ROOT

failures = []
blocked = []

def check(label, action):
    try:
        action()
    except ImportError as exc:
        blocked.append(label)
        print(f"BLOCKED {label}: {exc}")
    except Exception as exc:
        failures.append(label)
        print(f"FAIL {label}: {exc}")
    else:
        print(f"PASS {label}")

def require(condition, message):
    if not condition:
        raise ValueError(message)

def same(a, b):
    require(hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest(), str(b))

def skill_check(name):
    import yaml
    source = ROOT / "skills" / name
    target = PLUGIN / "skills" / name
    parts = (source / "SKILL.md").read_text(encoding="utf-8").split("---", 2)
    require(len(parts) == 3 and not parts[0].strip(), "missing YAML delimiters")
    header = yaml.safe_load(parts[1])
    require(header["name"] == name and bool(header["description"]), "invalid metadata")
    for rel in re.findall(r"`((?:assets|references|templates|scripts)/[^`]+|requirements-docx\.txt)`", parts[2]):
        require((source / rel).exists() and (target / rel).exists(), f"missing reference {rel}")
    same(source / "SKILL.md", target / "SKILL.md")
    for original in RESOURCES:
        relative = original.relative_to(ROOT)
        same(original, source / relative)
        same(original, target / relative)

def manifest_check():
    manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    require(manifest == json.loads((ROOT / "plugin-source.json").read_text(encoding="utf-8")), "generated manifest drift")
    require(manifest["version"] == "2.2.0" and manifest["skills"] == "./skills/", "wrong version or skills path")
    require({p.name for p in (PLUGIN / "skills").iterdir()} == set(NAMES), "unexpected plugin skills")
    for original in RESOURCES:
        same(original, PLUGIN / original.relative_to(ROOT))

def marketplace_check():
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    entry, = marketplace["plugins"]
    require(marketplace["name"] == "agent-engineering-toolkit", "wrong marketplace name")
    require(entry["name"] == "software-technical-docs-assistant", "wrong plugin name")
    require((ROOT / entry["source"]["path"]).resolve() == PLUGIN.resolve(), "incorrect marketplace target")

def scan():
    pattern = re.compile(r"gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|[A-Z]:\\Users\\", re.I)
    for base in (ROOT / "skills", PLUGIN):
        for path in base.rglob("*"):
            require(not path.is_symlink(), f"symlink: {path}")
            if path.is_file():
                require(not pattern.search(path.read_text(encoding="utf-8")), f"sensitive pattern: {path}")

def docs_check():
    for name in ("README.md", "README.zh-CN.md", "INSTALL.md", "CONTRIBUTING.md", "COMPATIBILITY.md"):
        content = (ROOT / name).read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", content):
            if not link.startswith(("https://", "http://", "#", "mailto:")):
                require((ROOT / link.split("#")[0]).exists(), f"{name}: broken link {link}")
    install = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
    for command in ("codex plugin marketplace add", "codex plugin add", "npx skills add", "--all -g", "--skill technical-architecture-design -g"):
        require(command in install, f"missing command {command}")

def docx_check():
    from docx import Document
    skill = PLUGIN / "skills" / NAMES[0]
    script = skill / "scripts/render_docx.py"
    ast.parse(script.read_text(encoding="utf-8"))
    require("python-docx" in (skill / "requirements-docx.txt").read_text(), "missing DOCX dependency")
    with tempfile.TemporaryDirectory(prefix="文档 test ") as directory:
        source = Path(directory) / "输入.md"
        output = Path(directory) / "输出.docx"
        fence = chr(96) * 3
        source.write_text("# 中文标题\n## Heading two\n普通 mixed **加粗** *斜体*\n| 名称 | Value |\n|---|---|\n| 中文 | true |\n- 项目\n1. 序号\n"
                          + fence + "cpp\nint main() {\n    return 0;\n}\n" + fence, encoding="utf-8")
        subprocess.run([sys.executable, str(script), str(source), "-o", str(output)], check=True)
        document = Document(output)
        require([p.style.name for p in document.paragraphs][:2] == ["Heading 1", "Heading 2"], "wrong headings")
        require(document.paragraphs[0].text == "中文标题", "wrong Chinese title")
        paragraph = document.paragraphs[2]
        require(paragraph.text == "普通 mixed 加粗 斜体", "incorrect paragraph")
        require(any(r.bold and r.text == "加粗" for r in paragraph.runs), "missing bold")
        require(any(r.italic and r.text == "斜体" for r in paragraph.runs), "missing italics")
        require(document.tables[0].cell(1, 0).text == "中文", "broken table")
        require([p.style.name for p in document.paragraphs][3:5] == ["List Bullet", "List Number"], "broken lists")
        require(document.paragraphs[-1].text == "int main() {\n    return 0;\n}", "broken code block")

for name in NAMES:
    check(f"frontmatter, references and SHA256: {name}", lambda: skill_check(name))
check("manifest and plugin resources", manifest_check)
check("marketplace", marketplace_check)
check("symlinks and sensitive patterns", scan)
check("documentation links and commands", docs_check)
check("DOCX reopening and document structure", docx_check)
sys.exit(1 if failures else 2 if blocked else 0)
