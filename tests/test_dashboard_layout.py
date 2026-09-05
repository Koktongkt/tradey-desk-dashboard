import re
import unittest
from pathlib import Path


INDEX = Path(__file__).resolve().parents[1] / "index.html"


class DashboardLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")

    def test_blocker_details_are_nested_in_matching_rejected_events(self):
        self.assertIn("const attachBlockerDiagnostics=", self.html)
        self.assertIn('<details class="event-diagnostics">', self.html)
        self.assertIn("<summary>Blocker details</summary>", self.html)
        self.assertIn("eventRows(orders)", self.html)
        self.assertNotIn('id="diagnostic-events"', self.html)
        self.assertNotIn('<details class="blocker-details">', self.html)

    def test_recent_activity_uses_two_flexible_columns(self):
        self.assertIn(
            ".activity{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}",
            self.html,
        )

    def test_blocker_matching_requires_rejection_reason_symbol_and_time(self):
        matcher = re.search(
            r"const attachBlockerDiagnostics=.*?;\nconst eventRows=",
            self.html,
        )
        self.assertIsNotNone(matcher)
        if matcher is None:
            self.fail("Blocker matcher was not found")
        source = matcher.group(0)
        for condition in (
            "row.status!=='rejected'",
            "gap>=0&&gap<=60000",
            "reasonCodes(row).includes(diag.reason)",
            "row.symbol===diag.symbol",
        ):
            self.assertIn(condition, source)


if __name__ == "__main__":
    unittest.main()
