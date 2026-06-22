# memory_service.py

import requests

from database import SessionLocal
from models import Memory
from vector_store import save_memory_embedding, save_summary_embedding
from models import Conversation
from vector_store import (
    save_conversation_embedding
)
from models import ConversationSummary

OLLAMA_URL = "http://localhost:11434/api/generate"
PROFILE_CATEGORIES = [
    "profession",
    "company",
    "diet",
    "location"
]

SINGLE_VALUE_CATEGORIES = [
    "profession",
    "company",
    "diet",
    "location"
]

MULTI_VALUE_CATEGORIES = [
    "goal",
    "friend",
    "project"
]

# -------------------------
# Memory Storage
# -------------------------

def save_memory(category, content):

    db = SessionLocal()

    try:

        if category in SINGLE_VALUE_CATEGORIES:

            existing = (
                db.query(Memory)
                .filter(
                    Memory.category == category
                )
                .first()
            )

            if existing:

                existing.content = content

                db.commit()

                return existing.id

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
        content=content,
        confidence=100,
        importance=get_importance(category)
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
        count = (
        db.query(Conversation)
        .count()
    )
        if count % 5 == 0:
            generate_conversation_summary()
        db.refresh(conversation)

        save_conversation_embedding(
            conversation.id,
            f"{role}: {message}"
        )

    finally:

        db.close()

def build_user_profile():

    memories = get_memories()

    profile = {}

    for m in memories:

        if m.category in profile:

            if isinstance(
                profile[m.category],
                list
            ):
                profile[m.category].append(
                    m.content
                )

            else:

                profile[m.category] = [
                    profile[m.category],
                    m.content
                ]

        else:

            profile[m.category] = m.content

    return profile

def get_recent_conversations(limit=20):

    db = SessionLocal()

    try:

        conversations = (
            db.query(Conversation)
            .order_by(
                Conversation.id.desc()
            )
            .limit(limit)
            .all()
        )

        return list(
            reversed(conversations)
        )

    finally:

        db.close()


def generate_conversation_summary():

    conversations = (
        get_recent_conversations(20)
    )

    if not conversations:
        return

    text = ""

    for c in conversations:

        text += (
            f"{c.role}: {c.message}\n"
        )

    prompt = f"""
Summarize these conversations.

Focus on:

- Goals
- Career
- Relationships
- Important events
- Personal preferences

Conversations:

{text}

Summary:
"""

    summary = ask_ollama(prompt)

    db = SessionLocal()

    try:

        summary_record = ConversationSummary(
summary=summary
)

        db.add(summary_record)

        db.commit()

        db.refresh(summary_record)

        save_summary_embedding(
            summary_record.id,
            summary
        )

    finally:
        db.close()


def get_importance(category):

    scores = {
        "profession": 10,
        "company": 9,
        "goal": 10,
        "diet": 7,
        "friend": 6,
        "project": 8,
        "location": 7
    }

    return scores.get(category, 5)

def build_user_profile():

    memories = get_memories()

    profile = {}

    for memory in memories:

        if memory.category not in PROFILE_CATEGORIES:
            continue

        profile[memory.category] = memory.content

    return profile

def get_goals():

    memories = get_memories()

    return [
        m.content
        for m in memories
        if m.category == "goal"
    ]

def get_friends():

    memories = get_memories()

    return [
        m.content
        for m in memories
        if m.category == "friend"
    ]

def build_full_profile():

    return {
        "profile": build_user_profile(),
        "goals": get_goals(),
        "friends": get_friends()
    }