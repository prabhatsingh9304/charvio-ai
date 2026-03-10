from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.suggestion import SuggestionRequest, SuggestionResponse, SuggestionUsed
from app.services.suggestion_service import suggestion_service
from app.api.session import sessions


router = APIRouter(prefix="/suggestions", tags=["suggestions"])


@router.post("", response_model=SuggestionResponse)
async def get_suggestions(request: SuggestionRequest, db: AsyncSession = Depends(get_db)):
    """
    Generate contextual conversation suggestions for the user.
    
    This endpoint analyzes the current session state including:
    - Character personality and background
    - Scene context and state
    - Conversation history
    
    And generates appropriate conversation starters that match the character
    and scene context. Suggestions are saved to the database for analytics.
    
    Args:
        request: SuggestionRequest containing session_id and num_suggestions
        db: Database session (injected)
    
    Returns:
        SuggestionResponse with list of contextual suggestions with IDs
    """
    # Get session
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = sessions[request.session_id]
    
    # Get primary character (first character in the scene)
    # In future, this could be enhanced to support multiple characters
    characters = state["characters"]
    if not characters:
        raise HTTPException(status_code=400, detail="No characters in session")
    
    # Get first character
    character_id = list(characters.keys())[0]
    character = characters[character_id]
    
    try:
        # Generate suggestions with database persistence
        suggestions = await suggestion_service.generate_suggestions(
            db=db,
            session_id=str(request.session_id),
            character_id=UUID(character_id),
            character_name=character["name"],
            personality=character["personality"],
            background=character["background"],
            scene_id=UUID(state["scene_id"]),
            scene_name=state["scene_name"],
            scene_description=state["scene_description"],
            scene_vars=state["scene_vars"],
            history=state["history"],
            num_suggestions=request.num_suggestions,
        )
        
        return SuggestionResponse(
            session_id=request.session_id,
            suggestions=suggestions,
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating suggestions: {str(e)}"
        )


@router.post("/{suggestion_id}/use", response_model=SuggestionUsed)
async def mark_suggestion_used(suggestion_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Mark a suggestion as used when the user clicks it.
    
    This helps track which suggestions are most effective and can be used
    for analytics and improving suggestion quality over time.
    
    Args:
        suggestion_id: ID of the suggestion to mark as used
        db: Database session (injected)
    
    Returns:
        SuggestionUsed response indicating success or failure
    """
    try:
        success = await suggestion_service.mark_suggestion_used(db, suggestion_id)
        
        if success:
            return SuggestionUsed(
                success=True,
                message="Suggestion marked as used"
            )
        else:
            raise HTTPException(
                status_code=404,
                detail="Suggestion not found"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error marking suggestion as used: {str(e)}"
        )
