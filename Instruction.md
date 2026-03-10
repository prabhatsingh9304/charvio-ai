# 📘 PROJECT_GUIDE.md
## Scalable Roleplay Conversation Engine
### FastAPI · PostgreSQL · Alembic · Pydantic · LangGraph · OpenRouter · Docker · Cursor

---

## 1. Project Vision

Build a **scalable, data-driven conversational roleplay engine** where:

- Any **scene**, **character**, or **story arc** can be added **without code changes**
- Users interact via chat and influence the narrative
- The system supports **multiple characters, narration, and branching outcomes**
- Architecture follows **clean Low-Level Design (LLD)**
- Token usage is **strictly optimized**
- Cursor generates code **without hallucinating architecture**

This file is the **single source of truth** for humans and Cursor.

---

## 2. Fixed Tech Stack (Non-Negotiable)

| Layer | Technology |
|-----|-----------|
| API | FastAPI |
| Validation | Pydantic |
| Database | PostgreSQL |
| Migrations | Alembic |
| Orchestration | LangGraph |
| LLM Gateway | OpenRouter |
| Containerization | Docker + Docker Compose |
| AI Coding | Cursor |

❌ No alternate frameworks  
❌ No client-side LLM calls  
❌ No hidden state machines  

---

## 3. Core Engineering Philosophy

> **LLMs generate language, not logic.**

All of the following MUST live in **code**, never in prompts:
- Control flow
- Speaker selection
- Scene transitions
- Exit conditions
- Validation
- Rule enforcement

LLMs are used ONLY for:
- Dialogue
- Descriptions
- Narrative prose

---

## 4. High-Level Architecture

Client (Chat UI)
↓
FastAPI (API Layer)
↓
LangGraph (Stateful Story Engine)
↓
OpenRouter (LLM Inference)
↓
PostgreSQL (Scenes, Characters, Memory)



### Responsibility Split
- **FastAPI** → HTTP, sessions, request lifecycle
- **Pydantic** → input/output validation
- **LangGraph** → story flow & state transitions
- **OpenRouter** → text generation only
- **PostgreSQL** → single source of truth

---

## 5. Mandatory Project Structure

Cursor MUST generate code using **exactly** this structure:

```
app/
├── api/
│ ├── chat.py # user chat endpoint
│ ├── session.py # start/load roleplay session
│
├── core/
│ ├── graph.py # LangGraph wiring
│ ├── state.py # runtime state (TypedDict)
│ ├── director.py # speaker & flow logic
│
├── nodes/
│ ├── narrator.py
│ ├── character.py
│
├── prompts/
│ ├── system.md
│ ├── narrator.md
│ ├── character.md
│ ├── director.md
│
├── models/ # SQLAlchemy ORM models
│ ├── base.py
│ ├── scene.py
│ ├── character.py
│
├── schemas/ # Pydantic models
│ ├── scene.py
│ ├── character.py
│ ├── chat.py
│
├── db/
│ ├── session.py # DB session
│ ├── repositories/
│ └── migrations/ # Alembic
│
├── services/
│ ├── llm.py # OpenRouter client
│
├── utils/
│ ├── prompt_builder.py
│ ├── token_budget.py
│
├── main.py
│
├── Dockerfile
├── docker-compose.yml
└── alembic.ini
```


❌ No prompts inside Python files  
❌ No business logic inside API routes  
❌ No story logic outside LangGraph  

---

## 6. Runtime State Pattern (LLD – STRICT)

LangGraph state contains **ONLY mutable runtime data**.

```python
class StoryState(TypedDict):
    session_id: str
    scene_id: str
    scene_vars: dict
    characters: dict
    history: list[str]
    user_input: str
    tension: int
    flags: dict
    next_actor: str
```
---
❌ Forbidden in State

Prompt templates

Character definitions

Scene definitions

Narrative rules

Static configuration
---




