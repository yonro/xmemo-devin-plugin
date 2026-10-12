from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    manifest_path = ROOT / ".devin-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    required = {"name", "displayName", "description", "homepage", "repository", "logo", "keywords", "mcpServers"}
    if set(manifest) != required:
        fail(f"manifest keys must be exactly {sorted(required)}")
    if manifest["name"] != "xmemo-devin" or manifest["mcpServers"].get("xmemo", {}).get("url") != "https://xmemo.dev/mcp":
        fail("manifest identity or MCP URL is invalid")
    if not (ROOT / manifest["logo"]).is_file():
        fail("manifest logo does not exist")
    if set(manifest["mcpServers"]) != {"xmemo"}:
        fail("manifest must declare exactly one xmemo server")
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    expected = {"xmemo-recall", "xmemo-checkpoint", "xmemo-handoff", "xmemo-resume"}
    if {p.parent.name for p in skills} != expected:
        fail("skill set does not match the four supported Devin workflows")
    for path in skills:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            fail(f"missing frontmatter: {path}")
        if not re.search(r"(?m)^name:\s+\S+", text) or not re.search(r"(?m)^description:\s+\S+", text):
            fail(f"invalid frontmatter: {path}")
    tracked = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    secret = re.compile(r"(?i)(gh[pousr]_[A-Za-z0-9_\-]{20,}|sk-[A-Za-z0-9]{20,}|xox[baprs]-|BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY)")
    for path in tracked:
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}:
            continue
        if secret.search(path.read_text(encoding="utf-8", errors="ignore")):
            fail(f"possible credential pattern in {path}")
    print(f"validated manifest, {len(skills)} skills, logo, references, and secret patterns")


if __name__ == "__main__":
    main()
