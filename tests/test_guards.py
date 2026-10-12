import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_package as validator
from release_gate import check


class Guards(unittest.TestCase):
    def test_candidate_allowed(self):
        check("v1.0.0-rc.2", "1.0.0-rc.2")

    def test_ga_and_malformed_rejected(self):
        for version in ["1.0.0", "1.1.0", "1.0.0-rc.0", "garbage"]:
            with self.subTest(version=version), self.assertRaises(ValueError):
                check("v" + version, version)

    def test_mismatched_tag(self):
        with self.assertRaises(ValueError):
            check("v1.0.0-rc.1", "1.0.0-rc.2")

    def test_reject_mutations(self):
        for mutation in ["credential", "logo_escape", "broken_link", "skill_drift", "source_drift", "version", "scopes", "license", "auto_approve", "skill_name"]:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "package"
                shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "dist"))
                manifest = root / ".devin-plugin/plugin.json"
                data = json.loads(manifest.read_text())
                if mutation == "credential":
                    data["mcpServers"]["xmemo"]["headers"] = {"Authorization": "Bearer synthetic"}
                if mutation == "logo_escape":
                    data["logo"] = "../logo.png"
                if mutation == "version":
                    data["version"] = "9.0.0"
                if mutation == "scopes":
                    data["mcpServers"]["xmemo"]["oauthScopes"].append("knowledge:write")
                if mutation == "license":
                    data["license"] = "UNLICENSED"
                recall = root / "skills/xmemo-recall/SKILL.md"
                if mutation == "auto_approve":
                    recall.write_text(recall.read_text().replace("name: xmemo-recall", "allowed-tools: '*'\nname: xmemo-recall"))
                if mutation == "skill_name":
                    recall.write_text(recall.read_text().replace("name: xmemo-recall", "name: wrong"))
                manifest.write_text(json.dumps(data))
                targets = {"broken_link": "README.md", "skill_drift": "skills/xmemo-handoff/SKILL.md", "source_drift": "vendor/claude/skills/handoff-work/SKILL.md"}
                if mutation in targets:
                    with (root / targets[mutation]).open("a") as f:
                        f.write("[broken](missing.md)" if mutation == "broken_link" else "drift")
                with patch.object(validator, "ROOT", root), self.assertRaises((SystemExit, ValueError)):
                    validator.main()
