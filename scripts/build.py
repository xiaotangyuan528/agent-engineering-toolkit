from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
NAMES = (

    "technical-implementation-documentation",
    "technical-document-review",
)
PLUGIN = ROOT / "plugins/codex"
RESOURCES = [*sorted((ROOT / "assets/templates").glob("*.md")),
             ROOT / "scripts/render_docx.py", ROOT / "requirements-docx.txt"]

def copy_checked(source, target):
    if source.is_symlink() or target.is_symlink():
        raise ValueError(f"Symlink in package: {source} -> {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    digest = lambda path: hashlib.sha256(path.read_bytes()).digest()
    if digest(source) != digest(target):
        raise ValueError(f"SHA256 mismatch: {target}")

def build():
    import yaml
    for name in NAMES:
        source = ROOT / "skills" / name / "SKILL.md"
        header = yaml.safe_load(source.read_text(encoding="utf-8").split("---", 2)[1])
        if header.get("name") != name or not header.get("description"):
            raise ValueError(f"Invalid frontmatter: {source}")
    for source in RESOURCES:
        if not source.is_file():
            raise ValueError(f"Missing source: {source}")
    print("PASS source frontmatter and resources")
    legacy = PLUGIN / "skills"
    if legacy.is_symlink() or (legacy.is_file() and legacy.read_text().strip() == "../../skills"):
        legacy.unlink()
    for name in NAMES:
        skill = ROOT / "skills" / name
        for source in RESOURCES:
            copy_checked(source, skill / source.relative_to(ROOT))
        for source in sorted(skill.rglob("*")):
            if source.is_file() and "__pycache__" not in source.parts:
                copy_checked(source, PLUGIN / "skills" / name / source.relative_to(skill))
    for source in RESOURCES:
        copy_checked(source, PLUGIN / source.relative_to(ROOT))
    manifest = json.loads((ROOT / "plugin-source.json").read_text(encoding="utf-8"))
    output = PLUGIN / ".codex-plugin/plugin.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS generated standalone skills and Codex package with SHA256 checks")

if __name__ == "__main__":
    try:
        build()
    except ImportError as exc:
        raise SystemExit(f"BLOCKED build dependency: {exc}")
    except (ValueError, OSError, KeyError, IndexError) as exc:
        raise SystemExit(f"FAIL build: {exc}")
