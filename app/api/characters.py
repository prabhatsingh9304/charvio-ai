from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.repositories.character_repository import character_repository
from app.db.repositories.scene_repository import scene_repository
from app.schemas.character import CharacterCreate, CharacterUpdate, CharacterResponse

router = APIRouter(prefix="/characters", tags=["characters"])


@router.post("", response_model=CharacterResponse, status_code=201)
async def create_character(
    character_data: CharacterCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new character.
    
    Characters are data-driven and can be added without code changes.
    """
    # Verify scene exists
    scene = await scene_repository.get_by_id(db, character_data.scene_id)
    if not scene:
        raise HTTPException(
            status_code=404,
            detail=f"Scene with id '{character_data.scene_id}' not found"
        )
    
    character = await character_repository.create(db, character_data)
    return character


@router.get("", response_model=List[CharacterResponse])
async def list_characters(
    scene_id: UUID = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all characters with optional filtering by scene.
    
    Query params:
    - scene_id: Filter by scene (optional)
    - skip: Pagination offset
    - limit: Pagination limit
    """
    if scene_id:
        characters = await character_repository.get_by_scene(db, scene_id)
    else:
        characters = await character_repository.get_all(db, skip=skip, limit=limit)
    
    return characters


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(
    character_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific character by ID."""
    character = await character_repository.get_by_id(db, character_id)
    
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    return character


@router.put("/{character_id}", response_model=CharacterResponse)
async def update_character(
    character_id: UUID,
    character_data: CharacterUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a character."""
    # If updating scene_id, verify new scene exists
    if character_data.scene_id:
        scene = await scene_repository.get_by_id(db, character_data.scene_id)
        if not scene:
            raise HTTPException(
                status_code=404,
                detail=f"Scene with id '{character_data.scene_id}' not found"
            )
    
    character = await character_repository.update(db, character_id, character_data)
    
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    return character


@router.delete("/{character_id}", status_code=204)
async def delete_character(
    character_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a character."""
    success = await character_repository.delete(db, character_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Character not found")
    
    return None
