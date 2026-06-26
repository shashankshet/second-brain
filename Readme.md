# 🧠 Second Brain

> A fully local, privacy-first AI assistant with long-term memory, semantic retrieval, conversation history, and personalized reasoning.

Second Brain is an AI-powered personal assistant that learns about you over time, remembers important facts, retrieves relevant conversations, summarizes long-term interactions, and answers questions using your personal context.

Unlike cloud-based AI assistants, **all data stays on your machine**.

No OpenAI API.

No external databases.

No cloud storage.

Everything runs locally using open-source models.

---

# Why Second Brain?

Most AI assistants are stateless—they forget everything after a conversation.

Second Brain is designed to become your **personal AI Chief of Staff**, capable of:

* Remembering who you are
* Tracking long-term goals
* Recalling past conversations
* Understanding relationships
* Building a persistent profile
* Providing personalized recommendations
* Running completely offline

---

# Features

## 🧠 Persistent Memory

Extracts and stores important facts about the user.

Example:

```text
User:
I am a backend engineer.

Stored:
profession → backend engineer
```

---

## 💬 Conversation Memory

Stores every user and assistant interaction.

Later:

```text
What did I tell you about Germany?
```

The assistant retrieves the relevant conversation instead of guessing.

---

## 🔎 Semantic Search

Uses sentence embeddings and ChromaDB to retrieve only the most relevant memories instead of sending everything to the LLM.

Technology:

* Sentence Transformers
* ChromaDB
* Vector Search

---

## 📚 Long-Term Conversation Summaries

Automatically summarizes conversations after a configurable number of chats.

Instead of searching hundreds of messages, the assistant searches concise summaries.

Example summary:

```text
Career:
Preparing for Google interviews

Fitness:
Started muscle gain plan

Personal:
Visited Germany for work

Goals:
1Cr salary
```

---

## 👤 Dynamic User Profile

Builds a persistent profile of the user.

Example:

```json
{
  "profession": "Backend Engineer",
  "company": "Siemens",
  "diet": "Vegetarian",
  "goals": [
    "1Cr Salary"
  ]
}
```

---

## 🔄 Memory Updates

Supports updating user attributes such as:

* Profession
* Company
* Diet
* Location

instead of storing duplicate memories.

---

## 🔐 Privacy First

Everything runs locally.

No user data leaves your computer.

No API keys required.

---

# Tech Stack

## Frontend

* Next.js
* React
* TypeScript

## Backend

* FastAPI
* SQLAlchemy
* SQLite

## AI

* Ollama
* Phi-3 / Qwen2.5
* Sentence Transformers

## Vector Database

* ChromaDB

---

# Architecture

```text
                    +----------------------+
                    |     Next.js UI       |
                    +----------+-----------+
                               |
                               |
                    FastAPI REST API
                               |
        +----------------------+----------------------+
        |                                             |
        |                                             |
 Fact Extraction                             Conversation Storage
        |                                             |
        |                                             |
   SQLite Database                             SQLite Database
        |                                             |
        +----------------------+----------------------+
                               |
                      Embedding Generation
                               |
                     Sentence Transformers
                               |
                         ChromaDB Vector DB
                               |
             +-----------------+-----------------+
             |                 |                 |
         Facts Search   Conversation Search  Summary Search
             |                 |                 |
             +-----------------+-----------------+
                               |
                     Context Construction
                               |
                         Ollama (Phi3/Qwen)
                               |
                        Personalized Response
```

---

# Current Project Structure

```text
second-brain/

├── backend/
│   ├── app.py
│   ├── database.py
│   ├── memory_service.py
│   ├── vector_store.py
│   ├── models.py
│   ├── schemas.py
│   └── memory.db
│
├── frontend/
│   ├── app/
│   ├── components/
│   └── package.json
│
└── README.md
```

---

# Memory Layers

Second Brain stores three different kinds of memory.

## 1. Facts

Structured information.

Examples:

```text
Profession
Company
Goals
Diet
Friends
```

---

## 2. Conversations

Complete chat history.

Example:

```text
User:
I visited Germany in March.

Assistant:
That's great! How was your trip?
```

---

## 3. Summaries

Compressed long-term memory.

Example:

```text
June Summary

Career:
Google Interview Preparation

Travel:
Germany

Fitness:
Bulking Journey
```

---

# API Endpoints

## Chat

```
POST /chat
```

---

## Memories

```
GET /memories
```

Returns all structured memories.

---

## Conversations

```
GET /conversations
```

Returns conversation history.

---

## Summaries

```
GET /summaries
```

Returns generated conversation summaries.

---

## Profile

```
GET /profile
```

Returns the current user profile.

---

## Debug Context

```
GET /debug-context
```

Displays the context being sent to the LLM.

---

## Reindex

```
GET /reindex
```

Rebuilds the vector database from stored memories.

---

# Running the Project

## Install Ollama

```bash
brew install ollama
```

Start Ollama

```bash
ollama serve
```

Pull a model

```bash
ollama pull phi3
```

or

```bash
ollama pull qwen2.5:7b
```

---

## Backend

```bash
cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Current Capabilities

* ✅ Local LLM
* ✅ Persistent Memory
* ✅ Fact Extraction
* ✅ Conversation Storage
* ✅ Conversation Retrieval
* ✅ Semantic Search
* ✅ Vector Embeddings
* ✅ Long-Term Summaries
* ✅ Dynamic User Profile
* ✅ Personalized Responses
* ✅ Fully Offline

---

# Future Roadmap

## Phase 6

* Memory conflict detection
* Memory confidence scores
* Memory importance ranking

## Phase 7

* Relationship extraction
* Entity recognition
* Dynamic knowledge graph

## Phase 8

* Neo4j integration
* Relationship reasoning

## Phase 9

* Document ingestion (PDF, Notes, Resume)
* Local RAG pipeline

## Phase 10

* Personal AI Agents

  * Career Agent
  * Health Agent
  * Finance Agent
  * Relationship Agent

## Phase 11

* Daily Briefings
* Weekly Summaries
* Proactive Suggestions
* Goal Tracking

---

# Vision

Second Brain is more than a chatbot.

It aims to become a **local AI operating system** that understands your life, remembers your experiences, and assists you in making better decisions while ensuring complete privacy.

---

# License

MIT License
