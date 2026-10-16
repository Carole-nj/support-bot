"""Core logic for a customer support chatbot.

The bot answers using the company knowledge base in faq.md. If the answer
is not in the knowledge base, it says so and offers a human handoff
instead of guessing.
"""
from pathlib import Path

import anthropic

MODEL = "claude-sonnet-5-5"
MAX_HISTORY = 20  # messages kept per conversation (keeps cost and latency down)

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

KNOWLEDGE_BASE = Path(__file__).with_name("faq.md").read_text(encoding="utf-8")

SYSTEM_PROMPT = f"""You are the customer support assistant for Acme Store.

Rules:
- Answer ONLY using the knowledge base below. Do not invent policies, prices or dates.
- If the answer is not in the knowledge base, say you are not sure and offer to
  connect the customer with a human agent (support@acme.example).
- Be friendly, concise and clear. Use short paragraphs.
- If the customer is angry or mentions a complaint, refund dispute or legal issue,
  apologise briefly and offer a human agent.
- Never ask for full card numbers or passwords.

<knowledge_base>
{KNOWLEDGE_BASE}
</knowledge_base>
"""

# In-memory conversation store: session_id -> list of messages.
# Use Redis or a database in production so history survives restarts.
_sessions: dict[str, list[dict]] = {}


def chat(session_id: str, user_message: str) -> str:
    history = _sessions.setdefault(session_id, [])
    history.append({"role": "user", "content": user_message})

    # Trim old messages, making sure the list starts with a user message.
    trimmed = history[-MAX_HISTORY:]
    while trimmed and trimmed[0]["role"] != "user":
        trimmed = trimmed[1:]

    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=trimmed,
    )
    answer = response.content[0].text
    history.append({"role": "assistant", "content": answer})
    return answer


def reset(session_id: str) -> None:
    _sessions.pop(session_id, None)


if __name__ == "__main__":
    # Quick terminal test: python support_bot.py
    sid = "terminal"
    while True:
        text = input("Customer: ")
        if text.lower() in {"quit", "exit"}:
            break
        print("Bot:", chat(sid, text))
