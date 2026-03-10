from typing import TypedDict


class StoryState(TypedDict):
    """
    Runtime state for LangGraph story engine.
    
    Contains ONLY mutable runtime data.
    NO prompts, character definitions, scene definitions, or static configuration.
    """
    session_id: str
    scene_id: str
    scene_name: str  # Scene name for prompt formatting
    scene_description: str  # Scene description for prompt formatting
    scene_vars: dict  # Runtime scene variables
    characters: dict  # Character IDs and current state
    history: list[str]  # Conversation history
    user_input: str  # Latest user message
    tension: int  # Story tension level (0-100)
    flags: dict  # Runtime flags for branching logic
    next_actor: str  # Who speaks next: "narrator", "character:<id>", "user"
    exit_conditions: dict  # Exit conditions for scene completion
