"""Tests for agent-forgetting-curve-governor."""
import unittest
from agent_forgetting_curve_governor.governor import ForgettingGovernor


class TestForgettingGovernor(unittest.TestCase):
    def setUp(self):
        self.gov = ForgettingGovernor(prune_threshold=0.5)

    def test_record_and_reinforce(self):
        item = self.gov.record_memory("key1", "val1", stability=1.0)
        self.assertEqual(item.access_count, 1)
        self.gov.recall_memory("key1")
        self.assertEqual(item.access_count, 2)
        self.assertGreater(item.stability, 1.0)

    def test_pruning(self):
        self.gov.record_memory("ephemeral", "data", stability=0.01)
        future_time = self.gov._items["ephemeral"].last_accessed + 50.0
        pruned = self.gov.prune(current_time=future_time)
        self.assertIn("ephemeral", pruned)


if __name__ == "__main__":
    unittest.main()
