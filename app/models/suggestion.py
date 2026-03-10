from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class Suggestion(BaseModel):
    """
    Suggestion model for storing generated user conversation suggestions.
    
    Tracks suggestions generated for users to help them start conversations
    with characters, including whether they were actually used.
    """
    
    __tablename__ = "suggestions"
    
    # Session ID (nullable - for tracking which session generated it)
    session_id = Column(String(36), nullable=True, index=True)
    
    # Foreign key to character
    character_id = Column(
        UUID(as_uuid=True),
        ForeignKey("characters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Foreign key to scene
    scene_id = Column(
        UUID(as_uuid=True),
        ForeignKey("scenes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # The actual suggestion text
    suggestion_text = Column(Text, nullable=False)
    
    # Hash of the context used to generate this suggestion (for deduplication/caching)
    context_hash = Column(String(64), nullable=True, index=True)
    
    # Whether the user clicked/used this suggestion
    was_used = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<Suggestion(id={self.id}, text='{self.suggestion_text[:30]}...', used={self.was_used})>"
