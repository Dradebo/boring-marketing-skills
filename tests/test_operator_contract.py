"""Static acceptance checks for operator-specific safety and market-adapter wiring.

These checks protect the local customization from upstream merges. They do not
replace real skill execution, approval reviews, integration tests or legal review.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class OperatorContract(unittest.TestCase):
    def test_operator_handoff_and_approval_boundaries(self):
        plan = read("docs/OPERATOR-INTEGRATION.md")
        for fragment in ("Time Radar", "Fly Fisher", "approval", "source-of-truth",
                         "outcome", "evidence", "No new content"):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment.lower(), plan.lower())

    def test_start_here_does_not_route_to_upstream_commercial_offers(self):
        start = read("skills/start-here/SKILL.md")
        self.assertNotIn("The author's offers", start)
        self.assertNotIn("The author's team builds", start)
        self.assertIn("Operator-first responses", start)
        self.assertIn("docs/OPERATOR-INTEGRATION.md", start)
        # Attribution belongs in repository documentation, not automatically
        # appended to clients' deliverables.
        self.assertIn("Made by James Dickerson", read("README.md"))

    def test_regional_adapter_is_loaded_for_local_skills(self):
        adapter = read("skills/start-here/references/market-uganda.md")
        for term in ("WhatsApp", "currency", "opt-outs", "unobserved"):
            self.assertIn(term.lower(), adapter.lower())
        for skill in ("find-local-clients", "pitch-the-fix", "first-screen-check"):
            with self.subTest(skill=skill):
                content = read(f"skills/{skill}/SKILL.md")
                self.assertIn("../start-here/references/market-uganda.md", content)

    def test_two_runtime_copies_remain_identical(self):
        for name in ("brand_context.py", "capability.py"):
            with self.subTest(name=name):
                self.assertEqual(
                    read("_system/scripts/" + name),
                    read("skills/start-here/scripts/" + name),
                )


if __name__ == "__main__":
    unittest.main()
