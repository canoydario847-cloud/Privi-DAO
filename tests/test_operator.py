import unittest
from unittest.mock import patch
from dao.operator import validate_target, proposals_for, run


class OperatorTests(unittest.TestCase):
    def test_reject_insecure_target(self):
        with self.assertRaises(ValueError):
            validate_target({"name": "internal", "url": "http://127.0.0.1:8000"})

    def test_reject_url_credentials(self):
        with self.assertRaises(ValueError):
            validate_target({"name": "x", "url": "https://user:pass@example.com"})

    def test_proposal_never_executes(self):
        result = [{"name": "example", "url": "https://example.com", "state": "unhealthy", "status_code": 503}]
        proposal = proposals_for(result, "sample-run")[0]
        self.assertEqual(proposal["status"], "proposed")
        self.assertEqual(proposal["execution"], "blocked_until_human_approval")

    @patch("dao.operator.inspect", return_value={"name": "example", "url": "https://example.com", "state": "healthy", "status_code": 200})
    def test_read_only_report(self, mocked):
        report = run({"targets": [{"name": "example", "url": "https://example.com"}]})
        self.assertEqual(report["mode"], "read_only")
        self.assertFalse(report["governance"]["autonomous_treasury_access"])
        self.assertEqual(report["proposals"], [])

    def test_duplicate_target_rejected(self):
        with self.assertRaises(ValueError):
            run({"targets": [{"name":"x", "url":"https://example.com"}, {"name":"x", "url":"https://example.org"}]})


if __name__ == "__main__":
    unittest.main()
