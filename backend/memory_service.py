# memory_service.py

import requests

from database import SessionLocal
from models import Memory
from vector_store import save_memory_embedding
from models import Conversation
from vector_store import (
    save_conversation_embedding
)

OLLAMA_URL = "http://localhost:11434/api/generate"


# -------------------------
# Memory Storage
# -------------------------

def save_memory(category, content):

    db = SessionLocal()

    try:

        existing = (
            db.query(Memory)
            .filter(
                Memory.category == category,
                Memory.content == content
            )
            .first()
        )

        if existing:
            return existing.id

        memory = Memory(
            category=category,
            content=content
        )

        db.add(memory)

        db.commit()

        db.refresh(memory)
        save_memory_embedding(
        memory.id,
        f"{category}: {content}"
    )

        return memory.id

    finally:
        db.close()


# -------------------------
# Simple Fact Extraction
# -------------------------

def extract_simple_fact(message):

    msg = message.lower().strip()

    if msg.startswith("i am a "):

        profession = msg.replace(
            "i am a ",
            ""
        ).strip()

        save_memory(
            "profession",
            profession
        )

    elif msg.startswith("i am an "):

        profession = msg.replace(
            "i am an ",
            ""
        ).strip()

        save_memory(
            "profession",
            profession
        )

    elif msg.startswith("i work at "):

        company = message[10:].strip()

        save_memory(
            "company",
            company
        )

    elif "vegetarian" in msg:

        save_memory(
            "diet",
            "vegetarian"
        )

    elif msg.startswith("i want "):

        goal = message[7:].strip()

        save_memory(
            "goal",
            goal
        )

    elif msg.startswith("my friend "):

        save_memory(
            "friend",
            message
        )


# -------------------------
# Process Message
# -------------------------

def process_message(message):

    extract_simple_fact(message)


# -------------------------
# Memory Retrieval
# -------------------------

def get_memories():

    db = SessionLocal()

    try:

        memories = db.query(Memory).all()

        return memories

    finally:

        db.close()


# -------------------------
# Context Builder
# -------------------------

def build_context():

    memories = get_memories()

    if not memories:
        return "No known facts."

    lines = []

    for m in memories:

        lines.append(
            f"- {m.category}: {m.content}"
        )

    return "\n".join(lines)


# -------------------------
# Ollama Chat
# -------------------------

def ask_ollama(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi3:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data.get(
        "response",
        "No response from model."
    )

def save_conversation(
    role,
    message
):

    db = SessionLocal()

    try:

        conversation = Conversation(
            role=role,
            message=message
        )

        db.add(conversation)

        db.commit()

        db.refresh(conversation)

        save_conversation_embedding(
            conversation.id,
            f"{role}: {message}"
        )

    finally:

        db.close()