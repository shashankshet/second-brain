# 🧠 Second Brain

A fully local, privacy-first AI personal assistant that continuously builds knowledge about you, remembers important facts, and helps you make better decisions.

Unlike cloud-based AI assistants, all data stays on your machine.

No OpenAI API.
No external services.
No data leaving your device.

Built using:

* Ollama
* FastAPI
* SQLite
* Next.js
* Python
* Open Source Models

---

# Vision

Most AI assistants forget everything between conversations.

Second Brain aims to become a personal operating system that:

* Learns about you
* Remembers important facts
* Tracks goals
* Understands relationships
* Stores long-term memory
* Provides personalized recommendations

All while running completely locally.

---

# Current Features

✅ Local LLM via Ollama

✅ Chat interface

✅ Persistent memory storage

✅ Fact extraction

✅ Context retrieval

✅ User profile memory

Example:

User:

```text
I am a backend engineer.
```

Stored Memory:

```text
profession: backend engineer
```

Later:

```text
Who am I?
```

Response:

```text
You are a backend engineer.
```

---

# Architecture

```text
┌───────────────┐
│   Next.js UI  │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   FastAPI     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    Ollama     │
│   Phi3/Qwen   │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    SQLite     │
└───────────────┘
```

---

# Project Structure

```text
second-brain/

├── backend/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── memory_service.py
│
├── frontend/
│   ├── app/
│   └── components/
│
└── data/
```

---

# Getting Started

## 1. Install Ollama

```bash
brew install ollama
```

Start Ollama:

```bash
ollama serve
```

Pull model:

```bash
ollama pull phi3
```

or

```bash
ollama pull qwen2.5:7b
```

---

## 2. Backend Setup

Create virtual environment:

```bash
cd backend

python3 -m venv venv

source venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy requests
```

Run backend:

```bash
uvicorn app:app --reload
```

Backend available at:

```text
http://localhost:8000
```

---

## 3. Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend available at:

```text
http://localhost:3000
```

---

# API Endpoints

## Chat

```http
POST /chat
```

Request:

```json
{
  "message": "Who am I?"
}
```

Response:

```json
{
  "response": "You are a backend engineer."
}
```

---

## Memories

```http
GET /memories
```

Returns all stored memories.

---

# Current Memory Model

```text
profession
diet
goal
friend
company
conversation
```

Example:

```text
profession: backend engineer

diet: vegetarian

goal: 1Cr salary
```

---

# Roadmap

## Phase 1

* [x] Local LLM
* [x] Memory Storage
* [x] Memory Retrieval
* [x] Chat UI

## Phase 2

* [ ] Conversation History
* [ ] Memory Deduplication
* [ ] Better Fact Extraction
* [ ] User Profile Generation

## Phase 3

* [ ] Semantic Search
* [ ] ChromaDB
* [ ] Embeddings
* [ ] Memory Ranking

## Phase 4

* [ ] Knowledge Graph
* [ ] Neo4j Integration
* [ ] Relationship Mapping
* [ ] Goal Tracking

## Phase 5

* [ ] Personal Agents
* [ ] Career Agent
* [ ] Health Agent
* [ ] Relationship Agent
* [ ] Daily Briefings

---

# Why Second Brain?

Most AI assistants answer questions.

Second Brain aims to understand the user.

The goal is to build a personal AI chief-of-staff that remembers your goals, projects, relationships, and decisions while keeping everything private and local.

---

# License

MIT License
