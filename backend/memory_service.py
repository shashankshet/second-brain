# memory_service.py

import requests
import json
from database import SessionLocal
from models import Memory

OLLAMA_URL = "http://localhost:11434/api/generate"

def extract_memory(message):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi3:latest",
            "prompt": message,
            "stream": False
        }
    )

    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    data = response.json()

    return data.get("response", "[]")

def save_memory(category, content):

    db = SessionLocal()

    existing = (
        db.query(Memory)
        .filter(
            Memory.category == category,
            Memory.content == content
        )
        .first()
    )

    if not existing:
        db.add(
            Memory(
                category=category,
                content=content
            )
        )
        db.commit()

    db.close()

def process_message(message):

    raw = extract_memory(message)

    try:

        memories = json.loads(raw)

        for m in memories:
            save_memory(
                m["category"],
                m["content"]
            )

    except:
        pass

def get_memories():

    db = SessionLocal()

    memories = db.query(Memory).all()

    db.close()

    return memories
def build_context():

    memories = get_memories()

    text = ""

    for m in memories:
        text += f"{m.category}: {m.content}\n"

    return text

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

    elif "vegetarian" in msg:

        save_memory(
            "diet",
            "vegetarian"
        )

    elif "want" in msg:

        save_memory(
            "goal",
            message
        )