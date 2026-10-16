# Customer Support Chatbot

A starter support bot that answers from your own FAQ (`faq.md`) using the Claude API.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"     # Windows PowerShell: $env:ANTHROPIC_API_KEY="your-key-here"
```

## Run

Terminal test:
```bash
python support_bot.py
```

Web chat (open http://localhost:8000):
```bash
uvicorn server:app --reload --port 8000
```

## Customise

1. Replace `faq.md` with your real policies, products and contact details.
2. Edit the company name and rules in `SYSTEM_PROMPT` in `support_bot.py`.
3. Set `allow_origins` in `server.py` to your website's domain.

## Before going live

- Store conversations in a database or Redis instead of the in-memory dict.
- Add rate limiting per IP/session to control cost and abuse.
- Add a human handoff (email, ticket system or live chat) when the bot cannot help.
- Log conversations (respecting privacy law) and review them to improve `faq.md`.
- For a large knowledge base, retrieve only the relevant sections per question instead of sending the whole file.
