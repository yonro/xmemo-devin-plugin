"""Deterministically adapt pinned MIT Claude workflows. Never edit generated files."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MAPPING = {"handoff-work": "xmemo-handoff", "resume-work": "xmemo-resume", "distill-session": "xmemo-checkpoint"}
def outputs(root=ROOT):
    lock=json.loads((root / "upstream-lock.json").read_text())
    for path, digest in lock["files"].items():
        raw=(root / "vendor/claude" / path).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=digest:
            raise ValueError("upstream digest mismatch: " + path)
    result={}
    for source, target in MAPPING.items():
        text=(root / "vendor/claude/skills" / source / "SKILL.md").read_text(encoding="utf-8")
        text=text.replace("name: " + source, "name: " + target).replace("Claude conversation", "Devin conversation").replace("Claude session", "Devin session")
        text=text.split("\nRead `../memory-steward/")[0]
        text += "\n\nRead [Devin safety and tool routing](../policy.md) before any operation. That policy governs authorization and capability availability for every step above.\n"
        result["skills/"+target+"/SKILL.md"]=text
    return result
if __name__=="__main__":
    import sys
    for path,text in outputs().items():
        p=ROOT/path
        if "--check" in sys.argv:
            if p.read_text(encoding="utf-8")!=text:
                raise SystemExit("Generated skill drift: " + path)
        else:
            p.write_text(text,encoding="utf-8",newline="\n")
