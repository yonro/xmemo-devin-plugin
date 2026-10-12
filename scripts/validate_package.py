from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    from sync_skills import outputs
    for path, expected_text in outputs(ROOT).items():
        if (ROOT / path).read_text(encoding="utf-8") != expected_text:
            fail("generated skill drift: " + path)
    manifest_path = ROOT / ".devin-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    required = {"name", "version", "description", "author", "homepage", "repository", "license", "logo", "keywords", "mcpServers"}
    if set(manifest) != required:
        fail(f"manifest keys must be exactly {sorted(required)}")
    if manifest["name"] != "xmemo" or manifest["mcpServers"].get("xmemo", {}).get("url") != "https://xmemo.dev/mcp":
        fail("manifest identity or MCP URL is invalid")
    if not re.fullmatch(r"[a-z0-9]+(?:[.-][a-z0-9]+)*", manifest["name"]):
        fail("manifest name must be lowercase alphanumeric with single - or . separators")
    version = (ROOT / "VERSION").read_text().strip()
    if manifest["version"] != version or not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
        fail("manifest version must match VERSION and use semver")
    if manifest["license"] != "MIT":
        fail("manifest license must match the distributed MIT license")
    if not isinstance(manifest.get("author"), dict) or "name" not in manifest["author"]:
        fail("manifest author must be an object with a name field")
    if manifest["mcpServers"] != {"xmemo": {"url": "https://xmemo.dev/mcp"}}:
        fail("MCP configuration must not embed credentials or override identity")
    logo = (ROOT / manifest["logo"]).resolve()
    if not logo.is_relative_to(ROOT.resolve()):
        fail("logo path escapes package")
    if not logo.is_file():
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
        frontmatter = text.split("---", 2)[1]
        if not re.search(r"(?m)^name: " + re.escape(path.parent.name) + r"$", frontmatter):
            fail(f"skill name must match directory: {path}")
        if "allowed-tools:" in frontmatter:
            fail("skills must not implicitly auto-approve tools")
    for path in [ROOT / "README.md", ROOT / "skills/policy.md", *skills]:
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            destination = (path.parent / target.split("#")[0]).resolve()
            if not destination.is_relative_to(ROOT.resolve()) or not destination.is_file():
                fail("broken or escaping reference: " + target)
    tracked = [p for p in ROOT.rglob("*") if p.is_file() and not set(p.parts) & {".git", "__pycache__", "dist"}]
    secret = re.compile(r"(?i)(gh[pousr]_[A-Za-z0-9_\-]{20,}|sk-[A-Za-z0-9]{20,}|xox[baprs]-|BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY)")
    for path in tracked:
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}:
            continue
        if secret.search(path.read_text(encoding="utf-8", errors="ignore")):
            fail(f"possible credential pattern in {path}")
    print(f"validated manifest, {len(skills)} skills, logo, references, and secret patterns")


if __name__ == "__main__":
    main()
