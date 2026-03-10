from uuid import UUID
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.suggestion import Suggestion


class SuggestionRepository:
    """Repository for Suggestion database operations."""
    
    async def create_batch(
        self,
        db: AsyncSession,
        suggestions_data: List[dict]
    ) -> List[Suggestion]:
        """
        Create multiple suggestions at once (bulk insert).
        
        Args:
            db: Database session
            suggestions_data: List of dicts with suggestion data
        
        Returns:
            List of created Suggestion objects
        """
        suggestions = [Suggestion(**data) for data in suggestions_data]
        db.add_all(suggestions)
        await db.flush()
        
        # Refresh all to get IDs and timestamps
        for suggestion in suggestions:
            await db.refresh(suggestion)
        
        return suggestions
    
    async def get_by_id(self, db: AsyncSession, suggestion_id: UUID) -> Optional[Suggestion]:
        """Get suggestion by ID."""
        result = await db.execute(
            select(Suggestion).where(Suggestion.id == suggestion_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_session(
        self,
        db: AsyncSession,
        session_id: str,
        limit: int = 100
    ) -> List[Suggestion]:
        """
        Get all suggestions for a session.
        
        Args:
            db: Database session
            session_id: Session ID to filter by
            limit: Maximum number of suggestions to return
        
        Returns:
            List of Suggestion objects
        """
        result = await db.execute(
            select(Suggestion)
            .where(Suggestion.session_id == session_id)
            .order_by(Suggestion.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def mark_as_used(
        self,
        db: AsyncSession,
        suggestion_id: UUID
    ) -> Optional[Suggestion]:
        """
        Mark a suggestion as used when user clicks it.
        
        Args:
            db: Database session
            suggestion_id: ID of the suggestion to mark
        
        Returns:
            Updated Suggestion object or None if not found
        """
        suggestion = await self.get_by_id(db, suggestion_id)
        
        if not suggestion:
            return None
        
        suggestion.was_used = True
        await db.flush()
        await db.refresh(suggestion)
        return suggestion
    
    async def get_by_context_hash(
        self,
        db: AsyncSession,
        context_hash: str,
        limit: int = 10
    ) -> List[Suggestion]:
        """
        Get suggestions by context hash (for potential caching/reuse).
        
        Args:
            db: Database session
            context_hash: Hash of the context
            limit: Maximum number of suggestions to return
        
        Returns:
            List of Suggestion objects with matching context hash
        """
        result = await db.execute(
            select(Suggestion)
            .where(Suggestion.context_hash == context_hash)
            .order_by(Suggestion.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_recent_by_character(
        self,
        db: AsyncSession,
        character_id: UUID,
        limit: int = 50
    ) -> List[Suggestion]:
        """
        Get recent suggestions for a character (for analytics).
        
        Args:
            db: Database session
            character_id: Character ID to filter by
            limit: Maximum number of suggestions to return
        
        Returns:
            List of recent Suggestion objects for the character
        """
        result = await db.execute(
            select(Suggestion)
            .where(Suggestion.character_id == character_id)
            .order_by(Suggestion.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()


# Global instance
suggestion_repository = SuggestionRepository()
