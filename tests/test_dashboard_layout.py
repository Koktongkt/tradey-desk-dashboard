import re
import unittest
from pathlib import Path


INDEX = Path(__file__).resolve().parents[1] / "index.html"


class DashboardLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")

    def test_blocker_details_are_collapsible_under_review_and_order_log(self):
        activity = re.search(
            r'<div class="panel activity">(?P<body>.*?)</div></section>\n <section class="section"><div class="section-head"><div><div class="eyebrow">Method, not marketing',
            self.html,
        )
        self.assertIsNotNone(activity, "Recent activity panel was not found")
        if activity is None:
            self.fail("Recent activity panel was not found")
        body = activity.group("body")
        review_heading = body.index("<h3>Review and order log</h3>")
        blocker_dropdown = body.index('<details class="blocker-details">')
        blocker_list = body.index('id="diagnostic-events"')

        self.assertLess(review_heading, blocker_dropdown)
        self.assertLess(blocker_dropdown, blocker_list)
        self.assertIn("<summary><span>Blocker details</span>", body)
        self.assertNotIn('<div class="activity-col"><h3>Blocker details</h3>', body)

    def test_recent_activity_uses_two_flexible_columns(self):
        self.assertIn(
            ".activity{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}",
            self.html,
        )

    def test_blocker_dropdown_count_tracks_filtered_diagnostics(self):
        self.assertIn(
            "document.querySelector('#blocker-detail-count').textContent=`${number(diagnostics.length)} record${diagnostics.length===1?'':'s'}`",
            self.html,
        )


if __name__ == "__main__":
    unittest.main()
