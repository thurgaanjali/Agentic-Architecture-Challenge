import unittest
from unittest.mock import patch

from part2.scraper import scrape_website, create_summary


class TestScraper(unittest.TestCase):

    def test_removes_unwanted_html(self):
        html = """
        <html>
            <body>
                <header>Website Header</header>
                <nav>Menu</nav>
                <main>This is the main content.</main>
                <footer>Footer</footer>
                <script>some code</script>
            </body>
        </html>
        """

        with patch("part2.scraper.requests.get") as mock_get:
            mock_get.return_value.text = html
            mock_get.return_value.raise_for_status.return_value = None

            result = scrape_website("https://example.com")

        self.assertIn("This is the main content.", result)
        self.assertNotIn("Website Header", result)
        self.assertNotIn("Menu", result)
        self.assertNotIn("Footer", result)

    def test_content_limit(self):
        long_text = "<main>" + ("word " * 3000) + "</main>"

        with patch("part2.scraper.requests.get") as mock_get:
            mock_get.return_value.text = long_text
            mock_get.return_value.raise_for_status.return_value = None

            result = scrape_website("https://example.com")

        self.assertLessEqual(len(result), 8000)

    def test_summary_limit(self):
        text = (
            "The company launched a new service for customers. "
            "The new service allows customers to manage their accounts online. "
            "Customers can also check their payment history. "
        )

        text = text * 50

        summary = create_summary(text)

        self.assertLessEqual(len(summary.split()), 120)

    def test_empty_content(self):
        result = create_summary("")

        self.assertEqual(result, "No content available.")


if __name__ == "__main__":
    unittest.main()