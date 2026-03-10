from uuid import UUID
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.scene import Scene
from app.schemas.scene import SceneCreate, SceneUpdate


class SceneRepository:
    """Repository for Scene database operations."""
    
    async def create(self, db: AsyncSession, scene_data: SceneCreate) -> Scene:
        """Create a new scene."""
        scene = Scene(**scene_data.model_dump())
        db.add(scene)
        await db.flush()
        await db.refresh(scene)
        return scene
    
    async def get_by_id(self, db: AsyncSession, scene_id: UUID) -> Optional[Scene]:
        """Get scene by ID."""
        result = await db.execute(
            select(Scene).where(Scene.id == scene_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Scene]:
        """Get scene by name."""
        result = await db.execute(
            select(Scene).where(Scene.name == name)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Scene]:
        """Get all scenes with pagination."""
        result = await db.execute(
            select(Scene).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def update(
        self,
        db: AsyncSession,
        scene_id: UUID,
        scene_data: SceneUpdate
    ) -> Optional[Scene]:
        """Update a scene."""
        scene = await self.get_by_id(db, scene_id)
        
        if not scene:
            return None
        
        update_data = scene_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(scene, field, value)
        
        await db.flush()
        await db.refresh(scene)
        return scene
    
    async def delete(self, db: AsyncSession, scene_id: UUID) -> bool:
        """Delete a scene."""
        scene = await self.get_by_id(db, scene_id)
        
        if not scene:
            return False
        
        await db.delete(scene)
        await db.flush()
        return True


# Global instance
scene_repository = SceneRepository()
