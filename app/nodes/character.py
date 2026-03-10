from app.core.state import StoryState
from app.services.llm import llm_client
from app.utils.prompt_builder import prompt_builder
from app.utils.token_budget import token_budget


async def character_node(state: StoryState) -> StoryState:
    """
    Character node: generates character dialogue.
    
    This node:
    1. Identifies which character should speak
    2. Loads character prompt template
    3. Formats with character personality and background
    4. Calls LLM for dialogue generation
    5. Updates state with character response
    """
    # Extract character ID from next_actor (format: "character:<id>")
    next_actor = state["next_actor"]
    
    if not next_actor.startswith("character:"):
        raise ValueError(f"Invalid next_actor for character node: {next_actor}")
    
    character_id = next_actor.split(":", 1)[1]
    
    # Get character data from state
    if character_id not in state["characters"]:
        raise ValueError(f"Character {character_id} not found in state")
    
    character_data = state["characters"][character_id]
    
    # Truncate history if needed
    truncated_history = token_budget.truncate_history(state["history"])
    
    # Format history for prompt
    history_text = "\n".join(truncated_history[-5:]) if truncated_history else "This is the beginning of the conversation."
    
    # Load system prompt
    system_prompt = prompt_builder.load_prompt("system")
    
    # Format character prompt
    character_prompt = prompt_builder.format_prompt(
        "character",
        character_name=character_data["name"],
        personality=character_data["personality"],
        background=character_data["background"],
        chats_example=character_data.get("chats_example", []),
        scene_name=state.get("scene_name", "Unknown Scene"),
        scene_description=state.get("scene_description", ""),
        scene_vars=str(state["scene_vars"]),
        history=history_text,
        user_input=state["user_input"],
    )
    
    # Build messages
    messages = prompt_builder.build_messages(
        system_prompt=system_prompt,
        user_prompt=character_prompt,
        history=None,  # History already included in character_prompt
    )
    
    # Generate response
    response = await llm_client.generate(messages)
    
    # Update state
    state["history"].append(f"{character_data['name']}: {response}")
    
    return state
