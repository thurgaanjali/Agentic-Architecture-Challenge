import unittest
from datetime import datetime, timedelta

from part1.routing import route_email


class TestRouting(unittest.TestCase):

    def test_billing(self):
        result = route_email("I was charged twice for my subscription.")
        self.assertEqual(result["route"], "automated_processing")
        self.assertEqual(result["category"], "Billing")

    def test_technical(self):
        result = route_email("I cannot login to my account because I get an error.")
        self.assertEqual(result["route"], "automated_processing")
        self.assertEqual(result["category"], "Technical")

    def test_feedback(self):
        result = route_email("I have a suggestion for improving the service.")
        self.assertEqual(result["route"], "automated_processing")
        self.assertEqual(result["category"], "Feedback")

    def test_security(self):
        result = route_email("Someone hacked my account and there was unauthorized access.")
        self.assertEqual(result["route"], "human_agent")
        self.assertTrue(result["critical"])

    def test_data_loss(self):
        result = route_email("I lost my data and some files are missing.")
        self.assertEqual(result["route"], "human_agent")
        self.assertTrue(result["critical"])

    def test_too_many_contacts(self):
        today = datetime.now()

        dates = [
            today - timedelta(days=1),
            today - timedelta(days=2),
            today - timedelta(days=3),
            today - timedelta(days=5)
        ]

        result = route_email("I need help with my account.", dates)

        self.assertEqual(result["route"], "human_agent")
        self.assertTrue(result["critical"])

    def test_refund(self):
        result = route_email("Can I get a RM500 refund?")

        self.assertEqual(result["route"], "human_agent")
        self.assertEqual(result["category"], "Billing")


if __name__ == "__main__":
    unittest.main()