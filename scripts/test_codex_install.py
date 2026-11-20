"""Install and verify the built plugin in a disposable CI runner."""
import json
import os
import shutil
import subprocess

from build import NAMES, ROOT

cli = shutil.which("codex.exe") or shutil.which("codex") or shutil.which("codex.cmd")
if not cli:
    raise SystemExit("BLOCKED Codex CLI missing")
if os.environ.get("GITHUB_ACTIONS") != "true":
    raise SystemExit("BLOCKED run on a disposable GitHub Actions runner")

plugin_id = "software-technical-docs-assistant@agent-engineering-toolkit"
subprocess.run([cli, "plugin", "marketplace", "add", str(ROOT)], check=True)
subprocess.run([cli, "plugin", "add", plugin_id, "--json"], check=True)
print("PASS Codex Marketplace and plugin install")
process = subprocess.Popen([cli, "app-server", "--stdio"], stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, text=True, encoding="utf-8")
try:
    def call(identifier, method, params):
        process.stdin.write(json.dumps(dict(id=identifier, method=method, params=params)) + "\n")
        process.stdin.flush()
        for line in process.stdout:
            message = json.loads(line)
            if message.get("id") == identifier:
                return message["result"]
        raise RuntimeError(f"No app-server reply: {method}")

    call(1, "initialize", {"clientInfo": {"name": "package_ci", "version": "1"},
                           "capabilities": {"experimentalApi": True}})
    result = call(2, "skills/list", {"cwds": [str(ROOT)], "forceReload": True})
    seen = {s["name"].split(":")[-1] for d in result["data"] for s in d["skills"]
            if s.get("pluginId") == plugin_id and s["enabled"]}
    if seen != set(NAMES):
        raise SystemExit(f"FAIL plugin skill discovery: {sorted(seen)}")
    print("PASS Codex discovered all five installed plugin skills")
finally:
    process.terminate()
    process.wait(timeout=10)
