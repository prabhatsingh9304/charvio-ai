from uuid import UUID
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterUpdate


class CharacterRepository:
    """Repository for Character database operations."""
    
    async def create(self, db: AsyncSession, character_data: CharacterCreate) -> Character:
        """Create a new character."""
        character = Character(**character_data.model_dump())
        db.add(character)
        await db.flush()
        await db.refresh(character)
        return character
    
    async def get_by_id(self, db: AsyncSession, character_id: UUID) -> Optional[Character]:
        """Get character by ID."""
        result = await db.execute(
            select(Character).where(Character.id == character_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_scene(self, db: AsyncSession, scene_id: UUID) -> List[Character]:
        """Get all characters for a scene."""
        result = await db.execute(
            select(Character).where(Character.scene_id == scene_id)
        )
        return result.scalars().all()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Character]:
        """Get all characters with pagination."""
        result = await db.execute(
            select(Character).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def update(
        self,
        db: AsyncSession,
        character_id: UUID,
        character_data: CharacterUpdate
    ) -> Optional[Character]:
        """Update a character."""
        character = await self.get_by_id(db, character_id)
        
        if not character:
            return None
        
        update_data = character_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(character, field, value)
        
        await db.flush()
        await db.refresh(character)
        return character
    
    async def delete(self, db: AsyncSession, character_id: UUID) -> bool:
        """Delete a character."""
        character = await self.get_by_id(db, character_id)
        
        if not character:
            return False
        
        await db.delete(character)
        await db.flush()
        return True


# Global instance
character_repository = CharacterRepository()
