from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.repositories.scene_repository import scene_repository
from app.schemas.scene import SceneCreate, SceneUpdate, SceneResponse

router = APIRouter(prefix="/scenes", tags=["scenes"])


@router.post("", response_model=SceneResponse, status_code=201)
async def create_scene(
    scene_data: SceneCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new scene.
    
    Scenes are data-driven and can be added without code changes.
    """
    # Check if scene with same name exists
    existing = await scene_repository.get_by_name(db, scene_data.name)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Scene with name '{scene_data.name}' already exists"
        )
    
    scene = await scene_repository.create(db, scene_data)
    return scene


@router.get("", response_model=List[SceneResponse])
async def list_scenes(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all scenes with pagination."""
    scenes = await scene_repository.get_all(db, skip=skip, limit=limit)
    return scenes


@router.get("/{scene_id}", response_model=SceneResponse)
async def get_scene(
    scene_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific scene by ID."""
    scene = await scene_repository.get_by_id(db, scene_id)
    
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    
    return scene


@router.put("/{scene_id}", response_model=SceneResponse)
async def update_scene(
    scene_id: UUID,
    scene_data: SceneUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a scene."""
    scene = await scene_repository.update(db, scene_id, scene_data)
    
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    
    return scene


@router.delete("/{scene_id}", status_code=204)
async def delete_scene(
    scene_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a scene and all its characters."""
    success = await scene_repository.delete(db, scene_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Scene not found")
    
    return None
