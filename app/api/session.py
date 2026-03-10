import uuid
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.repositories.scene_repository import scene_repository
from app.db.repositories.character_repository import character_repository
from app.schemas.chat import SessionCreate, SessionResponse

router = APIRouter(prefix="/session", tags=["session"])

# In-memory session storage (replace with Redis/database in production)
sessions: Dict[uuid.UUID, Dict] = {}


@router.post("/start", response_model=SessionResponse)
async def start_session(
    session_data: SessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Start a new roleplay session.
    
    Creates a new session with the specified scene and initializes state.
    """
    # Get scene from database
    scene = await scene_repository.get_by_id(db, session_data.scene_id)
    
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    
    # Get characters for this scene
    characters = await character_repository.get_by_scene(db, scene.id)
    
    # Create session ID
    session_id = uuid.uuid4()
    
    # Initialize session state
    session_state = {
        "session_id": str(session_id),
        "scene_id": str(scene.id),
        "scene_name": scene.name,
        "scene_description": scene.description,
        "scene_vars": scene.initial_state.copy(),
        "characters": {
            str(char.id): {
                "name": char.name,
                "personality": char.personality,
                "background": char.background,
                "chats_example": char.chats_example,
                "image": char.image,
            }
            for char in characters
        },
        "history": [],
        "user_input": "",
        "tension": 0,
        "flags": {},
        "next_actor": "narrator",
        "exit_conditions": scene.exit_conditions,
    }
    
    # Store session
    sessions[session_id] = session_state
    
    return SessionResponse(
        session_id=session_id,
        scene_id=scene.id,
        scene_vars=session_state["scene_vars"],
        characters=session_state["characters"],
        tension=session_state["tension"],
        next_actor=session_state["next_actor"],
    )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: uuid.UUID):
    """Get session state by ID."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = sessions[session_id]
    
    return SessionResponse(
        session_id=session_id,
        scene_id=uuid.UUID(state["scene_id"]),
        scene_vars=state["scene_vars"],
        characters=state["characters"],
        tension=state["tension"],
        next_actor=state["next_actor"],
    )
