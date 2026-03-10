from langgraph.graph import StateGraph, END
from app.core.state import StoryState
from app.core.director import director
from app.nodes.narrator import narrator_node
from app.nodes.character import character_node


def create_story_graph():
    """
    Create and configure the LangGraph story engine.
    
    Graph structure:
    - director_node: Determines next speaker (deterministic)
    - narrator_node: Generates narrative prose (LLM)
    - character_node: Generates character dialogue (LLM)
    
    Flow:
    1. User input arrives
    2. Director selects next speaker
    3. Route to appropriate node (narrator/character)
    4. Node generates response
    5. Return to director or end
    """
    
    # Create graph
    workflow = StateGraph(StoryState)
    
    # Add director node (deterministic logic)
    def director_node(state: StoryState) -> StoryState:
        """Director node: determines next speaker and updates tension."""
        # Update tension based on user input
        state["tension"] = director.update_tension(state, state["user_input"])
        
        # Select next speaker
        state["next_actor"] = director.select_next_speaker(state)
        
        return state
    
    # Add nodes
    workflow.add_node("director", director_node)
    workflow.add_node("narrator", narrator_node)
    workflow.add_node("character", character_node)
    
    # Set entry point
    workflow.set_entry_point("director")
    
    # Add conditional edges from director
    def route_from_director(state: StoryState) -> str:
        """Route to appropriate node based on next_actor."""
        next_actor = state["next_actor"]
        
        if next_actor == "narrator":
            return "narrator"
        elif next_actor.startswith("character:"):
            return "character"
        elif next_actor == "user":
            return END
        else:
            # Default to narrator
            return "narrator"
    
    workflow.add_conditional_edges(
        "director",
        route_from_director,
        {
            "narrator": "narrator",
            "character": "character",
            END: END,
        }
    )
    
    # After narrator/character, end (return control to user)
    workflow.add_edge("narrator", END)
    workflow.add_edge("character", END)
    
    # Compile graph
    app = workflow.compile()
    
    return app


# Global graph instance
story_graph = create_story_graph()
