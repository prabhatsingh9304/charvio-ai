# 🎭 Roleplay Conversation Engine

A **scalable, data-driven conversational roleplay engine** built with FastAPI, PostgreSQL, LangGraph, and OpenRouter.

## 🌟 Features

- **Data-Driven Design**: Add scenes and characters without code changes
- **LangGraph Orchestration**: Stateful story flow with deterministic control
- **Token Optimization**: Automatic history truncation and budget enforcement
- **Clean Architecture**: Separation of concerns between API, logic, and LLM calls
- **Async/Await**: High-performance async database and LLM operations

## 🏗️ Architecture

```
Client (Chat UI)
    ↓
FastAPI (API Layer)
    ↓
LangGraph (Stateful Story Engine)
    ↓
OpenRouter (LLM Inference)
    ↓
PostgreSQL (Scenes, Characters, Memory)
```

### Key Principles

- **LLMs generate language, not logic**: All control flow, speaker selection, and scene transitions are in code
- **Prompts in .md files**: Strict separation of prompts from Python code
- **Repository Pattern**: Clean data access layer
- **Type Safety**: Pydantic schemas for validation

## 📋 Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI |
| Validation | Pydantic |
| Database | PostgreSQL |
| Migrations | Alembic |
| Orchestration | LangGraph |
| LLM Gateway | OpenRouter |
| Containerization | Docker + Docker Compose |

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenRouter API key ([get one here](https://openrouter.ai/))

### Setup

1. **Clone the repository**
   ```bash
   cd sim-city
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` and add your OpenRouter API key**
   ```env
   OPENROUTER_API_KEY=your_key_here
   ```

4. **Start the services**
   ```bash
   docker-compose up -d
   ```

5. **Run database migrations**
   ```bash
   docker-compose exec app alembic upgrade head
   ```

6. **Load seed data**
   ```bash
   docker-compose exec db psql -U roleplay_user -d roleplay_db -f /app/seed_data.sql
   ```

7. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health

## 📖 API Usage

### 1. Start a Session

```bash
curl -X POST http://localhost:8000/session/start \
  -H "Content-Type: application/json" \
  -d '{
    "scene_id": "<scene_uuid>"
  }'
```

Response:
```json
{
  "session_id": "...",
  "scene_id": "...",
  "scene_vars": {...},
  "characters": {...},
  "tension": 0,
  "next_actor": "narrator"
}
```

### 2. Send a Chat Message

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "<session_uuid>",
    "message": "I walk into the tavern and look around."
  }'
```

Response:
```json
{
  "session_id": "...",
  "speaker": "narrator",
  "message": "The warm glow of firelight greets you as you push open the heavy oak door...",
  "tension": 0,
  "scene_vars": {...},
  "next_actor": "character:elara"
}
```

### 3. Get Session State

```bash
curl http://localhost:8000/session/<session_uuid>
```

## 🗂️ Project Structure

```
app/
├── api/              # FastAPI endpoints
│   ├── chat.py       # Chat endpoint
│   └── session.py    # Session management
├── core/             # Core logic
│   ├── config.py     # Configuration
│   ├── director.py   # Flow control (deterministic)
│   ├── graph.py      # LangGraph wiring
│   └── state.py      # Runtime state definition
├── nodes/            # LangGraph nodes
│   ├── narrator.py   # Narrator node
│   └── character.py  # Character node
├── prompts/          # Prompt templates (.md files)
│   ├── system.md
│   ├── narrator.md
│   ├── character.md
│   └── director.md
├── models/           # SQLAlchemy ORM models
│   ├── base.py
│   ├── scene.py
│   └── character.py
├── schemas/          # Pydantic schemas
│   ├── scene.py
│   ├── character.py
│   └── chat.py
├── db/               # Database layer
│   ├── session.py    # DB session management
│   ├── repositories/ # Repository pattern
│   └── migrations/   # Alembic migrations
├── services/         # External services
│   └── llm.py        # OpenRouter client
├── utils/            # Utilities
│   ├── prompt_builder.py
│   └── token_budget.py
└── main.py           # FastAPI app entry point
```

## 🔧 Development

### Create a New Migration

```bash
docker-compose exec app alembic revision --autogenerate -m "description"
```

### Apply Migrations

```bash
docker-compose exec app alembic upgrade head
```

### Rollback Migration

```bash
docker-compose exec app alembic downgrade -1
```

### View Logs

```bash
docker-compose logs -f app
```

## 🎨 Adding New Scenes

Scenes are data-driven! No code changes needed.

```sql
INSERT INTO scenes (id, name, description, initial_state, exit_conditions, created_at, updated_at)
VALUES (
    gen_random_uuid(),
    'Your Scene Name',
    'Scene description...',
    '{"key": "value"}',
    '{"condition": true}',
    NOW(),
    NOW()
);
```

## 👥 Adding New Characters

```sql
INSERT INTO characters (id, name, personality, background, scene_id, created_at, updated_at)
VALUES (
    gen_random_uuid(),
    'Character Name',
    'Personality description...',
    'Background story...',
    '<scene_uuid>',
    NOW(),
    NOW()
);
```

## 🧪 Testing

### Health Check

```bash
curl http://localhost:8000/health
```

### Interactive API Docs

Visit http://localhost:8000/docs for interactive Swagger UI.

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! Please follow the architectural principles outlined in `Instruction.md`.
