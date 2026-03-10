from uuid import UUID
from pydantic import BaseModel, Field
from typing import List


class SuggestionItem(BaseModel):
    """Individual suggestion with ID and text."""
    
    id: UUID
    text: str


class SuggestionRequest(BaseModel):
    """Schema for requesting user suggestions."""
    
    session_id: UUID
    num_suggestions: int = Field(default=3, ge=3, le=10, description="Number of suggestions to generate (3-10)")


class SuggestionResponse(BaseModel):
    """Schema for suggestion API response."""
    
    session_id: UUID
    suggestions: List[SuggestionItem] = Field(..., description="List of contextual conversation starters with IDs")


class SuggestionUsed(BaseModel):
    """Schema for marking a suggestion as used."""
    
    success: bool
    message: str
