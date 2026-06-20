from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, SessionLocal
from models import Base, Memory, Conversation
from schemas import ChatRequest
from vector_store import build_hybrid_context, build_relevant_context, save_memory_embedding
from memory_service import (
    process_message,
    build_context,
    ask_ollama,
    save_conversation
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
    save_conversation(
    "user",
    req.message
)
    process_message(req.message)

    context = build_hybrid_context(
    req.message
)

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
    print("QUERY:")
    print(req.message)

    print("RELEVANT CONTEXT:")
    print(context)
    response = ask_ollama(prompt)
    save_conversation(
    "assistant",
    response
)
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

@app.get("/reindex")
def reindex():

    db = SessionLocal()

    memories = db.query(Memory).all()

    for m in memories:

        save_memory_embedding(
            m.id,
            f"{m.category}: {m.content}"
        )

    db.close()

    return {"status": "done"}