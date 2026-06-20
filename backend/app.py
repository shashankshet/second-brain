from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, SessionLocal
from models import Base, Memory, Conversation
from schemas import ChatRequest

from memory_service import (
    process_message,
    build_context,
    ask_ollama
)
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

    prompt = f"""
You are Second Brain.

You are the user's private local AI assistant.

Known facts:

{context}

Answer naturally.

Do not output code.

Do not invent facts.

User:
{req.message}

Assistant:
"""

    response = ask_ollama(prompt)

    return {
        "response": response
    }

@app.get("/conversations")
def conversations():

    db = SessionLocal()

    data = db.query(Conversation).all()

    db.close()

    return [
        {
            "role": c.role,
            "message": c.message
        }
        for c in data
    ]