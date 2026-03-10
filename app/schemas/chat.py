from uuid import UUID
from pydantic import BaseModel, Field
from typing import Dict, Optional


class SessionCreate(BaseModel):
    """Schema for creating a new roleplay session."""
    
    scene_id: UUID


class SessionResponse(BaseModel):
    """Schema for session API response."""
    
    session_id: UUID
    scene_id: UUID
    scene_vars: Dict
    characters: Dict
    tension: int
    next_actor: str


class ChatRequest(BaseModel):
    """Schema for chat request."""
    
    session_id: UUID
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    """Schema for chat response."""
    
    session_id: UUID
    speaker: str  # "narrator", "character:<name>", "system"
    message: str
    tension: int
    scene_vars: Dict
    next_actor: str
