from typing import Dict, List
from app.core.state import StoryState


class Director:
    """
    Director handles deterministic story flow control.
    
    This is CODE-BASED logic, NOT LLM-based.
    Controls:
    - Speaker selection
    - Scene transitions
    - Exit condition evaluation
    - Flow decisions
    """
    
    def select_next_speaker(self, state: StoryState) -> str:
        """
        Determine who speaks next based on deterministic rules.
        
        Returns: "narrator", "character:<id>", or "user"
        """
        history_length = len(state["history"])
        
        # First interaction: narrator sets the scene
        if history_length == 0:
            return "narrator"
        
        # After user input, alternate between narrator and characters
        last_speaker = self._get_last_speaker(state)
        
        if last_speaker == "user":
            # User just spoke - prioritize character responses
            if state["characters"]:
                # Characters respond directly most of the time
                return self._select_character(state)
            else:
                # No characters available, narrator responds
                return "narrator"
        
        elif last_speaker == "narrator":
            # Narrator just spoke, character can respond
            if state["characters"]:
                return self._select_character(state)
            else:
                return "user"
        
        elif last_speaker.startswith("character:"):
            # Character just spoke, give control back to user
            return "user"
        
        # Default: if characters exist, use them; otherwise narrator
        if state["characters"]:
            return self._select_character(state)
        return "narrator"
    
    def _get_last_speaker(self, state: StoryState) -> str:
        """Extract the last speaker from history."""
        if not state["history"]:
            return "user"
        
        # History format: "speaker: message"
        last_entry = state["history"][-1]
        if ":" in last_entry:
            return last_entry.split(":", 1)[0].strip().lower()
        
        return "user"
    
    def _select_character(self, state: StoryState) -> str:
        """
        Select which character speaks next.
        
        For now, uses simple round-robin.
        Can be enhanced with more sophisticated logic.
        """
        characters = list(state["characters"].keys())
        
        if not characters:
            return "narrator"
        
        # Simple round-robin based on history length
        history_length = len(state["history"])
        char_index = history_length % len(characters)
        
        return f"character:{characters[char_index]}"
    
    def check_exit_conditions(self, state: StoryState, exit_conditions: Dict) -> bool:
        """
        Check if scene exit conditions are met.
        
        Exit conditions are evaluated against scene_vars.
        Example: {"quest_completed": True, "boss_defeated": True}
        """
        if not exit_conditions:
            return False
        
        scene_vars = state["scene_vars"]
        
        # All conditions must be met
        for key, expected_value in exit_conditions.items():
            if key not in scene_vars:
                return False
            if scene_vars[key] != expected_value:
                return False
        
        return True
    
    def update_tension(self, state: StoryState, user_input: str) -> int:
        """
        Update tension level based on user input and context.
        
        This is a simple heuristic. Can be enhanced with sentiment analysis.
        """
        current_tension = state["tension"]
        
        # Keywords that increase tension
        tension_keywords = ["attack", "fight", "run", "danger", "help", "urgent"]
        # Keywords that decrease tension
        calm_keywords = ["rest", "calm", "peace", "relax", "wait"]
        
        user_lower = user_input.lower()
        
        # Increase tension
        for keyword in tension_keywords:
            if keyword in user_lower:
                current_tension = min(100, current_tension + 10)
                break
        
        # Decrease tension
        for keyword in calm_keywords:
            if keyword in user_lower:
                current_tension = max(0, current_tension - 10)
                break
        
        # Natural decay over time (slight decrease each turn)
        current_tension = max(0, current_tension - 2)
        
        return current_tension


# Global instance
director = Director()
