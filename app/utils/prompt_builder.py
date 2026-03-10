from pathlib import Path
from typing import Dict, Any


class PromptBuilder:
    """
    Utility to load and format prompts from .md files.
    
    Prompts are stored in app/prompts/ directory as markdown files.
    This enforces separation of prompts from code logic.
    """
    
    def __init__(self, prompts_dir: str = "app/prompts"):
        """Initialize with prompts directory path."""
        self.prompts_dir = Path(prompts_dir)
    
    def load_prompt(self, prompt_name: str) -> str:
        """
        Load a prompt template from a .md file.
        
        Args:
            prompt_name: Name of the prompt file (without .md extension)
        
        Returns:
            Prompt template as string
        """
        prompt_path = self.prompts_dir / f"{prompt_name}.md"
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    
    def format_prompt(self, prompt_name: str, **kwargs: Any) -> str:
        """
        Load and format a prompt template with variables.
        
        Args:
            prompt_name: Name of the prompt file
            **kwargs: Variables to substitute in the template
        
        Returns:
            Formatted prompt string
        """
        template = self.load_prompt(prompt_name)
        
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(
                f"Missing required variable {e} for prompt '{prompt_name}'"
            )
    
    def build_messages(
        self,
        system_prompt: str,
        user_prompt: str,
        history: list[str] = None
    ) -> list[Dict[str, str]]:
        """
        Build message array for LLM API call.
        
        Args:
            system_prompt: System message
            user_prompt: User message
            history: Optional conversation history
        
        Returns:
            List of message dicts for LLM API
        """
        messages = [{"role": "system", "content": system_prompt}]
        
        if history:
            for i, msg in enumerate(history):
                role = "assistant" if i % 2 == 0 else "user"
                messages.append({"role": role, "content": msg})
        
        messages.append({"role": "user", "content": user_prompt})
        
        return messages


# Global instance
prompt_builder = PromptBuilder()
