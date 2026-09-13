from __future__ import annotations

import unittest

from scripts.build_repo_cards_snapshot import PLANNING_FIELDS, compact_fields


class SnapshotCompactionTests(unittest.TestCase):
    def test_repo_cards_do_not_duplicate_full_plans(self) -> None:
        planning = {
            "operator_queue": "ready-now",
            "workflow_sync_status": "matches",
            "repomap_snapshot": {"status": "present"},
            "proof_snapshot": {"status": "complete"},
            "plan": {"large": "internal plan payload"},
            "files": ["plan.json"],
        }

        compact = compact_fields(planning, PLANNING_FIELDS)

        self.assertEqual("ready-now", compact["operator_queue"])
        self.assertNotIn("plan", compact)
        self.assertNotIn("files", compact)


if __name__ == "__main__":
    unittest.main()
