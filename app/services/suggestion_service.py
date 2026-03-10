import json
import hashlib
from uuid import UUID
from pathlib import Path
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.llm import llm_client
from app.db.repositories.suggestion_repository import suggestion_repository
from app.schemas.suggestion import SuggestionItem


class SuggestionService:
    """
    Service for generating contextual user suggestions.
    
    Uses LLM to generate conversation starters based on:
    - Character personality and background
    - Scene context and state
    - Conversation history
    """
    
    def __init__(self):
        """Initialize suggestion service."""
        # Load suggestion prompt template
        prompt_path = Path(__file__).parent.parent / "prompts" / "suggestion.md"
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    async def generate_suggestions(
        self,
        db: AsyncSession,
        session_id: str,
        character_id: UUID,
        character_name: str,
        personality: str,
        background: str,
        scene_id: UUID,
        scene_name: str,
        scene_description: str,
        scene_vars: Dict,
        history: List[str],
        num_suggestions: int = 3,
    ) -> List[SuggestionItem]:
        """
        Generate contextual conversation suggestions and save to database.
        
        Args:
            db: Database session
            session_id: Session ID for tracking
            character_id: Character UUID
            character_name: Name of the character
            personality: Character's personality description
            background: Character's background story
            scene_id: Scene UUID
            scene_name: Name of the scene
            scene_description: Scene description
            scene_vars: Current scene state variables
            history: Conversation history (list of messages)
            num_suggestions: Number of suggestions to generate
        
        Returns:
            List of SuggestionItem objects with IDs and text
        """
        # Generate context hash for potential caching/deduplication
        context_hash = self._generate_context_hash(
            character_name, personality, scene_name, history
        )
        
        # Format history
        if history:
            history_text = "\n".join(history[-10:])  # Last 10 messages for context
        else:
            history_text = "(No conversation yet - this is the start of the interaction)"
        
        # Format scene vars
        scene_vars_text = json.dumps(scene_vars, indent=2) if scene_vars else "{}"
        
        # Build prompt
        prompt = self.prompt_template.format(
            character_name=character_name,
            personality=personality,
            background=background,
            scene_name=scene_name,
            scene_description=scene_description,
            scene_vars=scene_vars_text,
            history=history_text,
            num_suggestions=num_suggestions,
        )
        
        # Generate suggestions using LLM
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        
        try:
            response = await llm_client.generate(
                messages=messages,
                temperature=0.8,  # Higher temperature for more creative suggestions
                max_tokens=500,
            )
            
            # Parse JSON response
            # Remove markdown code blocks if present
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            suggestions = json.loads(response)
            
            # Validate response
            if not isinstance(suggestions, list):
                raise ValueError("Response is not a list")
            
            # Ensure we have the right number of suggestions
            if len(suggestions) < num_suggestions:
                # Pad with generic suggestions if needed
                suggestions.extend([
                    "Tell me more about yourself",
                    "What's on your mind?",
                    "**looks around** What should we do?",
                ][:num_suggestions - len(suggestions)])
            
            suggestion_texts = suggestions[:num_suggestions]
        
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Fallback to generic suggestions if parsing fails
            suggestion_texts = self._get_fallback_suggestions(character_name, num_suggestions)
        
        # Save suggestions to database
        suggestions_data = [
            {
                "session_id": session_id,
                "character_id": character_id,
                "scene_id": scene_id,
                "suggestion_text": text,
                "context_hash": context_hash,
                "was_used": False,
            }
            for text in suggestion_texts
        ]
        
        db_suggestions = await suggestion_repository.create_batch(db, suggestions_data)
        
        # Return as SuggestionItem objects
        return [
            SuggestionItem(id=sug.id, text=sug.suggestion_text)
            for sug in db_suggestions
        ]
    
    def _get_fallback_suggestions(self, character_name: str, num_suggestions: int) -> List[str]:
        """
        Generate fallback suggestions if LLM fails.
        
        Args:
            character_name: Name of the character
            num_suggestions: Number of suggestions needed
        
        Returns:
            List of generic suggestion strings
        """
        fallback = [
            f"Hello, {character_name}!",
            "Tell me about yourself",
            "What brings you here?",
            "**smiles** Nice to meet you",
            "What's your story?",
            "I'd like to know more about you",
            "**looks around curiously**",
            "What should we talk about?",
        ]
        
        return fallback[:num_suggestions]
    
    def _generate_context_hash(self, character_name: str, personality: str, scene_name: str, history: List[str]) -> str:
        """
        Generate a hash of the context for deduplication/caching.
        
        Args:
            character_name: Name of the character
            personality: Character's personality
            scene_name: Name of the scene
            history: Conversation history
        
        Returns:
            SHA256 hash of the context
        """
        # Create a string representation of the context
        context_str = f"{character_name}|{personality}|{scene_name}|{'|'.join(history[-5:])}"
        
        # Generate SHA256 hash
        return hashlib.sha256(context_str.encode()).hexdigest()
    
    async def mark_suggestion_used(self, db: AsyncSession, suggestion_id: UUID) -> bool:
        """
        Mark a suggestion as used when user clicks it.
        
        Args:
            db: Database session
            suggestion_id: ID of the suggestion to mark
        
        Returns:
            True if successful, False if suggestion not found
        """
        result = await suggestion_repository.mark_as_used(db, suggestion_id)
        return result is not None


# Global instance
suggestion_service = SuggestionService()
