from app.core.state import StoryState
from app.services.llm import llm_client
from app.utils.prompt_builder import prompt_builder
from app.utils.token_budget import token_budget


async def narrator_node(state: StoryState) -> StoryState:
    """
    Narrator node: generates narrative prose.
    
    This node:
    1. Loads narrator prompt template
    2. Formats with scene context and history
    3. Calls LLM for narrative generation
    4. Updates state with narrator response
    """
    # Truncate history if needed
    truncated_history = token_budget.truncate_history(state["history"])
    
    # Format history for prompt
    history_text = "\n".join(truncated_history[-5:]) if truncated_history else "This is the beginning of the story."
    
    # Load system prompt
    system_prompt = prompt_builder.load_prompt("system")
    
    # Format narrator prompt
    narrator_prompt = prompt_builder.format_prompt(
        "narrator",
        scene_name=state.get("scene_name", "Unknown Scene"),
        scene_description=state.get("scene_description", ""),
        scene_vars=str(state["scene_vars"]),
        history=history_text,
        user_input=state["user_input"],
    )
    
    # Build messages
    messages = prompt_builder.build_messages(
        system_prompt=system_prompt,
        user_prompt=narrator_prompt,
        history=None,  # History already included in narrator_prompt
    )
    
    # Generate response
    response = await llm_client.generate(messages)
    
    # Update state
    state["history"].append(f"Narrator: {response}")
    
    return state
