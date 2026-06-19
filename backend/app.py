from fastapi import FastAPI

from fastapi import FastAPI
from memory_service import build_context, extract_simple_fact, extract_simple_fact, process_message, save_memory, save_memory
from schemas import ChatRequest
from database import engine
from models import Base
from database import SessionLocal
from models import Memory
import requests
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Second Brain Backend Running"
    }

@app.get("/memories")
def memories():

    db = SessionLocal()

    data = db.query(Memory).all()

    db.close()

    return [
        {
            "id": m.id,
            "category": m.category,
            "content": m.content
        }
        for m in data
    ]

@app.post("/chat")
def chat(req: ChatRequest):
    process_message(req.message)
    context = build_context()
    save_memory(
    "conversation",
    req.message
)
    print("CONTEXT:")
    print(context)

    prompt = f"""
You are Second Brain.

You are the user's private local AI assistant.

Known facts about the user:

{context}

Answer naturally.

Do not output code.

Do not invent facts.

User:
{req.message}

Assistant:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return {
        "response": data.get("response", "No response")
    }