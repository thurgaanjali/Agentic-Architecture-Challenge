import re
import requests
from bs4 import BeautifulSoup
from collections import Counter


MAX_CONTENT_LENGTH = 8000
MAX_SUMMARY_WORDS = 120


def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as error:
        print("Could not access the website:", error)
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    main_content = soup.find("main")

    if main_content is None:
        main_content = soup.find("article")

    if main_content is None:
        main_content = soup.body

    if main_content is None:
        return ""

    text = main_content.get_text(" ", strip=True)

    if len(text) > MAX_CONTENT_LENGTH:
        text = text[:MAX_CONTENT_LENGTH]

    return text


def create_summary(text):
    if text == "":
        return "No content available."

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    if len(sentences) <= 1:
        words = text.split()
        return " ".join(words[:MAX_SUMMARY_WORDS])

    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    word_counts = Counter(words)

    scored_sentences = []

    for position, sentence in enumerate(sentences):
        sentence_words = re.findall(
            r"\b[a-zA-Z]{3,}\b",
            sentence.lower()
        )

        score = 0

        for word in sentence_words:
            score += word_counts[word]

        scored_sentences.append((score, position, sentence))

    scored_sentences.sort(reverse=True)

    selected = []

    for score, position, sentence in scored_sentences:
        selected.append((position, sentence))

        current_text = " ".join(
            item[1] for item in sorted(selected)
        )

        if len(current_text.split()) >= MAX_SUMMARY_WORDS:
            break

    selected.sort()

    summary = " ".join(
        item[1] for item in selected
    )

    words = summary.split()

    if len(words) > MAX_SUMMARY_WORDS:
        summary = " ".join(words[:MAX_SUMMARY_WORDS])

    return summary


if __name__ == "__main__":
    url = "https://example.com"

    content = scrape_website(url)
    summary = create_summary(content)

    print("\nSummary:")
    print(summary)