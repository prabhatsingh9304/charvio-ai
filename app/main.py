from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import session, chat, scenes, characters, prompts, upload, auth, suggestions
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for FastAPI application."""
    # Startup
    print("🚀 Starting Roleplay Conversation Engine...")
    print(f"📊 Environment: {settings.APP_ENV}")
    print(f"🤖 LLM Model: {settings.LLM_MODEL}")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title="Roleplay Conversation Engine",
    description="Scalable, data-driven conversational roleplay engine",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(session.router)
app.include_router(chat.router)
app.include_router(scenes.router)
app.include_router(characters.router)
app.include_router(prompts.router)
app.include_router(upload.router)
app.include_router(suggestions.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Roleplay Conversation Engine API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
