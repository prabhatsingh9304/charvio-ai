from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.graph import story_graph
from app.api.session import sessions

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process user chat message and generate response.
    
    Flow:
    1. Retrieve session state
    2. Update with user input
    3. Execute LangGraph
    4. Return response
    """
    # Get session
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = sessions[request.session_id]
    
    # Update state with user input
    state["user_input"] = request.message
    state["history"].append(f"User: {request.message}")
    
    # Execute LangGraph
    try:
        result = await story_graph.ainvoke(state)
        
        # Update session with result
        sessions[request.session_id] = result
        
        # Extract response message
        # The last entry in history is the generated response
        if result["history"]:
            last_message = result["history"][-1]
            
            # Parse speaker and message
            if ":" in last_message:
                speaker, message = last_message.split(":", 1)
                speaker = speaker.strip()
                message = message.strip()
            else:
                speaker = "system"
                message = last_message
        else:
            speaker = "system"
            message = "No response generated"
        
        return ChatResponse(
            session_id=request.session_id,
            speaker=speaker.lower(),
            message=message,
            tension=result["tension"],
            scene_vars=result["scene_vars"],
            next_actor=result["next_actor"],
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat: {str(e)}"
        )
