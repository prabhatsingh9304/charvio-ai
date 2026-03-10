import tiktoken
from typing import List
from app.core.config import settings


class TokenBudget:
    """
    Token tracking and budget enforcement.
    
    Ensures LLM calls stay within token limits by:
    - Counting tokens in messages
    - Truncating/summarizing history when approaching limits
    - Logging token usage per session
    """
    
    def __init__(self, model: str = "gpt-4"):
        """Initialize with tiktoken encoding for the model."""
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base for unknown models
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string."""
        return len(self.encoding.encode(text))
    
    def count_messages_tokens(self, messages: List[str]) -> int:
        """Count total tokens in a list of messages."""
        return sum(self.count_tokens(msg) for msg in messages)
    
    def truncate_history(
        self,
        history: List[str],
        max_tokens: int = None
    ) -> List[str]:
        """
        Truncate history to stay within token budget.
        
        Keeps most recent messages and removes oldest ones.
        """
        if max_tokens is None:
            max_tokens = settings.HISTORY_TRUNCATE_THRESHOLD
        
        total_tokens = self.count_messages_tokens(history)
        
        if total_tokens <= max_tokens:
            return history
        
        # Keep removing oldest messages until we're under budget
        truncated = history.copy()
        while total_tokens > max_tokens and len(truncated) > 1:
            removed = truncated.pop(0)
            total_tokens -= self.count_tokens(removed)
        
        # Add indicator that history was truncated
        if len(truncated) < len(history):
            truncated.insert(0, "[Earlier conversation truncated...]")
        
        return truncated
    
    def check_budget(
        self,
        prompt: str,
        history: List[str],
        max_context_tokens: int = None,
        max_response_tokens: int = None
    ) -> bool:
        """
        Check if a prompt + history fits within token budget.
        
        Returns True if within budget, False otherwise.
        """
        if max_context_tokens is None:
            max_context_tokens = settings.MAX_CONTEXT_TOKENS
        if max_response_tokens is None:
            max_response_tokens = settings.MAX_RESPONSE_TOKENS
        
        prompt_tokens = self.count_tokens(prompt)
        history_tokens = self.count_messages_tokens(history)
        
        total_tokens = prompt_tokens + history_tokens + max_response_tokens
        
        return total_tokens <= max_context_tokens


# Global instance
token_budget = TokenBudget()
