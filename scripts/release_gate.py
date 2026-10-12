"""Fail closed: this candidate line cannot publish GA before a reviewed gate change."""
import re
from pathlib import Path
def check(tag, version):
    if not re.fullmatch(r"1\.0\.0-rc\.[1-9][0-9]*", version):
        raise ValueError("GA blocked: real Devin OAuth, isolation, revoke and session evidence required")
    if tag != "v"+version:
        raise ValueError("tag/version mismatch")
if __name__=="__main__":
    import sys
    check(sys.argv[1], (Path(__file__).resolve().parents[1]/"VERSION").read_text().strip())
