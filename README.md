# Agentic Architect Challenge

A small prototype covering customer support routing, web scraping, and a stateful agent workflow.

## Project Structure

```text
agentic-architect-challenge/
├── part1/
│   ├── architecture.md
│   ├── routing.py
│   └── knowledge_base/
│       └── support_faq.txt
├── part2/
│   ├── README.md
│   └── scraper.py
├── part3/
│   ├── agent.py
│   └── knowledge_base/
│       └── support_guide.txt
├── tests/
│   ├── test_routing.py
│   ├── test_scraper.py
│   └── test_agent.py
├── docs/
│   └── architecture_summary.pdf
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.13 or compatible Python 3 version
- Internet connection is required for Part 2 website scraping

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run All Tests

From the project root:

```powershell
python -m unittest discover -s tests -v
```

The current test suite contains 15 tests covering the main required behaviours.

## Part 1 - Customer Support Email Processing

Part 1 checks critical conditions before generating a response. Critical cases include data loss, service outages, security issues, and more than three support contacts within seven days.

Normal emails are classified into Billing, Technical, Feedback, or General Support.

The system uses a local FAQ file and takes a conservative approach to refund requests. When the knowledge base does not provide enough information, the case is escalated instead of making up an answer.

Run:

```powershell
python part1\routing.py
```

## Part 2 - Web Scraping and Summarization

The scraper removes unnecessary HTML elements, prefers the main page content, handles request errors, and uses a 10-second timeout.

Guardrails:

- Maximum scraped content: 8,000 characters
- Maximum summary length: 120 words

The current prototype uses a simple extractive summarization method so it does not require an external LLM API.

Run:

```powershell
python part2\scraper.py
```

## Part 3 - LangGraph Agent

Part 3 uses LangGraph with in-memory checkpointing.

The agent can:

- Answer questions from the sample support document
- Remember the user's name during the conversation
- Use a calculator when arithmetic is requested
- Refuse to invent information that is not in the support guide

Run:

```powershell
python part3\agent.py
```

The current Part 3 implementation is a deterministic local prototype. An LLM adapter can be added later without changing the document, memory, or tool boundaries.

## Security

API keys must not be stored in source files or committed to GitHub. Use environment variables for any future external LLM integration.

Example:

```powershell
$env:OPENAI_API_KEY="YOUR_KEY"
```

Do not commit `.env`, API keys, or the `.venv` folder.

## Assumption for Part 2

The assessment description refers to a starter scraper that was not included with the materials available during development. Therefore, a minimal intentionally flawed scraper was created first so the scraping bottleneck and improvements could be demonstrated and tested.

## Known Limitations

- Part 1 uses keyword-based classification and critical detection.
- Part 2 does not use a browser engine, so JavaScript-heavy pages may not expose their main content.
- Part 3 is currently deterministic and local rather than LLM-generated.
- In-memory conversation state is lost when the program stops.

## Production Improvements

For a production deployment, the next improvements would be structured logging, metrics, tracing, retry policies, persistent conversation storage, confidence thresholds, stronger document retrieval, and an LLM adapter with output validation.
