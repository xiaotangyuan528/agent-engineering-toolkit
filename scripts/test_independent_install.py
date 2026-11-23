import os
from pathlib import Path
import subprocess
import sys
import tempfile

from build import NAMES, RESOURCES, ROOT

def install(root, prefix, flags, names):
    with tempfile.TemporaryDirectory() as directory:
        home = Path(directory) / "home"
        home.mkdir()
        env = dict(os.environ, HOME=str(home), USERPROFILE=str(home), XDG_CONFIG_HOME=str(home / ".config"))
        command = [*prefix, "--yes", "skills", "add", str(root), *flags, "-a", "codex", "-y"]
        subprocess.run(command, cwd=directory, env=env, check=True)
        installed = home / ".agents/skills" if "-g" in flags else Path(directory) / ".agents/skills"
        if {path.name for path in installed.iterdir()} != set(names):
            raise ValueError(f"Unexpected installed skill set: {installed}")
        for name in names:
            for relative in [Path("SKILL.md"), *(path.relative_to(ROOT) for path in RESOURCES)]:
                if (installed / name / relative).read_bytes() != (ROOT / "skills" / name / relative).read_bytes():
                    raise ValueError(f"Installed content mismatch: {name}/{relative}")
        print(f"PASS independent install: {', '.join(flags)}")

if __name__ == "__main__":
    prefix = sys.argv[1:] or (["npx.cmd"] if os.name == "nt" else ["npx"])
    try:
        install(ROOT, prefix, ["--all", "-g"], NAMES)
        install(ROOT, prefix, ["--skill", "technical-implementation-documentation", "-g"], ["technical-implementation-documentation"])
    except FileNotFoundError as exc:
        raise SystemExit(f"BLOCKED independent install: {exc}")
    except (ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"FAIL independent install: {exc}")
