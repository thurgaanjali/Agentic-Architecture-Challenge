import unittest

from part3.agent import ask_agent


class TestAgent(unittest.TestCase):

    def test_support_hours(self):
        answer = ask_agent(
            "What are the support hours?",
            "test-hours"
        )

        self.assertIn("Monday to Friday", answer)
        self.assertIn("9:00 AM to 6:00 PM", answer)

    def test_unknown_information(self):
        answer = ask_agent(
            "What is the price of a replacement laptop?",
            "test-unknown"
        )

        self.assertIn("not covered", answer.lower())

    def test_calculator(self):
        answer = ask_agent(
            "What is 25 multiplied by 8?",
            "test-calculator"
        )

        self.assertIn("200", answer)

    def test_memory(self):
        first_answer = ask_agent(
            "My name is Thurga.",
            "test-memory"
        )

        second_answer = ask_agent(
            "What is my name?",
            "test-memory"
        )

        self.assertIn("Thurga", first_answer)
        self.assertIn("Thurga", second_answer)


if __name__ == "__main__":
    unittest.main()