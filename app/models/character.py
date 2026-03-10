from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Character(BaseModel):
    """
    Character model representing a roleplay character.
    
    Characters are data-driven and can be added without code changes.
    """
    
    __tablename__ = "characters"
    
    name = Column(String(255), nullable=False, index=True)
    personality = Column(Text, nullable=False)
    background = Column(Text, nullable=False)
    image = Column(String, nullable=True)
    chats_example = Column(JSONB, nullable=True)
    
    # Foreign key to scene
    scene_id = Column(
        UUID(as_uuid=True),
        ForeignKey("scenes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Relationship to scene
    scene = relationship("Scene", back_populates="characters")
    
    def __repr__(self):
        return f"<Character(name={self.name}, scene_id={self.scene_id})>"
