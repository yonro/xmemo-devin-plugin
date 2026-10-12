import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_package


class PackageTests(unittest.TestCase):
    def test_package_validator(self):
        validate_package.main()

    def test_no_credentials_in_manifest(self):
        manifest = json.loads((ROOT / ".devin-plugin/plugin.json").read_text(encoding="utf-8-sig"))
        self.assertNotIn("headers", manifest["mcpServers"]["xmemo"])
        self.assertNotIn("env", manifest["mcpServers"]["xmemo"])


if __name__ == "__main__":
    unittest.main()
