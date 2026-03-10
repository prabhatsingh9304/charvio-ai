from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Scene(BaseModel):
    """
    Scene model representing a roleplay scenario.
    
    Scenes are data-driven and can be added without code changes.
    """
    
    __tablename__ = "scenes"
    
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    image = Column(String, nullable=True)
    
    # Initial state variables for the scene (e.g., {"location": "tavern", "time": "evening"})
    initial_state = Column(JSONB, nullable=False, default=dict)
    
    # Exit conditions for scene completion (e.g., {"quest_completed": true})
    exit_conditions = Column(JSONB, nullable=False, default=dict)
    
    # Relationship to characters
    characters = relationship("Character", back_populates="scene", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Scene(name={self.name})>"
