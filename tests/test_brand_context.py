import subprocess, sys, tempfile, unittest
from pathlib import Path
SCRIPTS = Path(__file__).resolve().parents[1] / "_system" / "scripts"
SKILL = Path(__file__).resolve().parents[1] / "skills" / "direct-response-copy" / "SKILL.md"

def run(root):
    r = subprocess.run([sys.executable, str(SCRIPTS / "brand_context.py"), "--skill-file", str(SKILL), "--root", str(root)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout

class BrandContext(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp()); (self.root / "brand").mkdir()
        (self.root / "brand" / "positioning.md").write_text("# Positioning\nAngle: X\n")

    def test_marketing_md_first_then_preferences(self):
        (self.root / "MARKETING.md").write_text("Goal: leads. Never discount.\n")
        (self.root / "brand" / "preferences.md").write_text("Banned: 'unlock'\n")
        out = run(self.root)
        i_m, i_p, i_pos = out.index("MARKETING.md"), out.index("preferences.md"), out.index("positioning.md")
        self.assertTrue(i_m < i_p < i_pos)

    def test_marketing_md_truncates_at_300(self):
        (self.root / "MARKETING.md").write_text("\n".join(f"line {i}" for i in range(400)))
        out = run(self.root)
        self.assertIn("truncated at 300 lines", out); self.assertNotIn("line 350", out)

    def test_absent_files_unchanged(self):
        out = run(self.root)
        self.assertNotIn("MARKETING.md", out); self.assertNotIn("preferences.md", out)

    def test_brand_env_flag_without_values(self):
        (self.root / "brand" / ".env").write_text("KIT_API_KEY=secret123\n")
        out = run(self.root)
        self.assertIn("brand .env present: yes", out); self.assertNotIn("secret123", out)

if __name__ == "__main__":
    unittest.main()
