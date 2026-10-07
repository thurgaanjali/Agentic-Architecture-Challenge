# Part 2 - Web Scraping and Concise Summarization

## Objective

The goal of this part is to scrape useful content from a website and create a concise summary.

The original approach had a problem because it extracted the entire webpage text without filtering unnecessary content. Long webpages could therefore produce a very large amount of text for the summarization step.

## Problems Identified

The basic scraper had several limitations:

* It extracted text from the whole HTML page.
* It did not remove navigation, headers, footers, scripts, or styles.
* It had no limit on the amount of content processed.
* It had no timeout or HTTP error handling.
* It did not have a limit on the final summary length.

The main bottleneck is processing too much irrelevant webpage content.

## Improvements

The scraper was improved by:

1. Removing unnecessary HTML elements such as `script`, `style`, `nav`, `header`, and `footer`.
2. Looking for the main page content using `main`, `article`, or `body`.
3. Limiting scraped content to 8,000 characters.
4. Adding a 10-second request timeout.
5. Handling request errors safely.
6. Using extractive summarization to select important sentences.
7. Limiting the final summary to 120 words.

## Processing Flow

```text
Website
   |
   v
Download HTML
   |
   v
Remove unnecessary HTML
   |
   v
Extract main content
   |
   v
Limit input to 8,000 characters
   |
   v
Select important sentences
   |
   v
Limit summary to 120 words
   |
   v
Final Summary
```

## Summary Method

The current prototype uses a simple extractive summarization method.

It counts important words in the webpage and gives each sentence a score based on those words. Higher-scoring sentences are selected for the summary and then returned in their original order.

This approach does not require an external AI API, which keeps the prototype simple and easy to run locally.

## Guardrails

Two limits are used:

```text
Maximum webpage content: 8,000 characters
Maximum summary length: 120 words
```

These limits help prevent very large webpages from creating unnecessarily large processing workloads and keep the final output concise.

## Trade-offs

The extractive approach is lightweight and does not require an API key, but it is less natural than an LLM-generated summary.

For a production system, an LLM could be used after the scraping stage. The existing input and output limits should still be kept as guardrails.

## Testing

Part 2 includes tests for:

* Removing unwanted HTML elements.
* Limiting webpage content.
* Limiting summary length.
* Handling empty content.

Run all project tests from the project root:

```powershell
python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 11 tests
OK
```

## Running Part 2

From the project root:

```powershell
python part2/scraper.py
```

The program downloads the example website and prints the generated summary.

## Dependencies

Part 2 uses:

* Python
* requests
* beautifulsoup4
