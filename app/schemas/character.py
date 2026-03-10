from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CharacterBase(BaseModel):
    """Base schema for Character with shared fields."""
    
    name: str = Field(..., min_length=1, max_length=255)
    personality: str = Field(..., min_length=1)
    background: str = Field(..., min_length=1)
    image: Optional[str] = None
    chats_example: Optional[Any] = None
    scene_id: UUID


class CharacterCreate(CharacterBase):
    """Schema for creating a new Character."""
    pass


class CharacterUpdate(BaseModel):
    """Schema for updating a Character."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    personality: Optional[str] = Field(None, min_length=1)
    background: Optional[str] = Field(None, min_length=1)
    image: Optional[str] = Field(None)
    chats_example: Optional[Any] = Field(None)
    scene_id: Optional[UUID] = None


class CharacterResponse(CharacterBase):
    """Schema for Character API response."""
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
