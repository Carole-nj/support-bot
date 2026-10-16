"""Web API for the support bot. Run with: uvicorn server:app --reload"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

import support_bot

app = FastAPI(title="Support Bot")

# Restrict this to your real website domain(s) before going live.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        return ChatResponse(reply=support_bot.chat(req.session_id, req.message))
    except Exception:
        raise HTTPException(status_code=502, detail="The assistant is unavailable right now.")


@app.get("/", response_class=HTMLResponse)
def index():
    return Path(__file__).with_name("index.html").read_text(encoding="utf-8")
