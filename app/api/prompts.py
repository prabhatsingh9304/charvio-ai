from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path

router = APIRouter(prefix="/prompts", tags=["prompts"])

PROMPTS_DIR = Path("app/prompts")


class PromptResponse(BaseModel):
    """Response model for prompt content."""
    name: str
    content: str


class PromptUpdate(BaseModel):
    """Request model for updating prompts."""
    content: str


@router.get("", response_model=list[str])
async def list_prompts():
    """
    List all available prompt files.
    
    Returns list of prompt names (without .md extension).
    """
    if not PROMPTS_DIR.exists():
        raise HTTPException(status_code=500, detail="Prompts directory not found")
    
    prompts = [f.stem for f in PROMPTS_DIR.glob("*.md")]
    return prompts


@router.get("/{prompt_name}", response_model=PromptResponse)
async def get_prompt(prompt_name: str):
    """
    Get the content of a specific prompt.
    
    Available prompts: system, narrator, character, director
    """
    prompt_path = PROMPTS_DIR / f"{prompt_name}.md"
    
    if not prompt_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Prompt '{prompt_name}' not found. Available: system, narrator, character, director"
        )
    
    try:
        content = prompt_path.read_text(encoding="utf-8")
        return PromptResponse(name=prompt_name, content=content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading prompt: {str(e)}"
        )


@router.put("/{prompt_name}", response_model=PromptResponse)
async def update_prompt(prompt_name: str, prompt_data: PromptUpdate):
    """
    Update a prompt file.
    
    Note: Changes take effect after restarting the app.
    """
    prompt_path = PROMPTS_DIR / f"{prompt_name}.md"
    
    if not prompt_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Prompt '{prompt_name}' not found. Available: system, narrator, character, director"
        )
    
    try:
        # Backup current prompt
        backup_path = PROMPTS_DIR / f"{prompt_name}.md.backup"
        if prompt_path.exists():
            backup_path.write_text(prompt_path.read_text(encoding="utf-8"), encoding="utf-8")
        
        # Write new content
        prompt_path.write_text(prompt_data.content, encoding="utf-8")
        
        return PromptResponse(name=prompt_name, content=prompt_data.content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating prompt: {str(e)}"
        )


@router.post("/{prompt_name}/restore", response_model=PromptResponse)
async def restore_prompt_backup(prompt_name: str):
    """
    Restore a prompt from its backup.
    
    Useful if you made a mistake and want to revert changes.
    """
    prompt_path = PROMPTS_DIR / f"{prompt_name}.md"
    backup_path = PROMPTS_DIR / f"{prompt_name}.md.backup"
    
    if not backup_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"No backup found for prompt '{prompt_name}'"
        )
    
    try:
        content = backup_path.read_text(encoding="utf-8")
        prompt_path.write_text(content, encoding="utf-8")
        
        return PromptResponse(name=prompt_name, content=content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error restoring prompt: {str(e)}"
        )
