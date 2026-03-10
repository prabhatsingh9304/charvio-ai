from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Optional


class SceneBase(BaseModel):
    """Base schema for Scene with shared fields."""
    
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    image: Optional[str] = None
    initial_state: Dict = Field(default_factory=dict)
    exit_conditions: Dict = Field(default_factory=dict)


class SceneCreate(SceneBase):
    """Schema for creating a new Scene."""
    pass


class SceneUpdate(BaseModel):
    """Schema for updating a Scene."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    image: Optional[str] = None
    initial_state: Optional[Dict] = None
    exit_conditions: Optional[Dict] = None


class SceneResponse(SceneBase):
    """Schema for Scene API response."""
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
