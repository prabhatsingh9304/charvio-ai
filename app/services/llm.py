import httpx
from typing import List, Dict, Optional
from app.core.config import settings


class OpenRouterClient:
    """
    OpenRouter LLM client service.
    
    Handles all LLM API calls with:
    - Async HTTP requests
    - Error handling and retries
    - Model selection
    """
    
    def __init__(self):
        """Initialize OpenRouter client."""
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL
        self.base_url = settings.LLM_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = None,
        temperature: float = 0.7,
        model: Optional[str] = None,
    ) -> str:
        """
        Generate text using OpenRouter API.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            model: Override default model
        
        Returns:
            Generated text
        """
        if max_tokens is None:
            max_tokens = settings.MAX_RESPONSE_TOKENS
        
        if model is None:
            model = self.model
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                )
                response.raise_for_status()
                
                data = response.json()
                return data["choices"][0]["message"]["content"]
            
            except httpx.HTTPStatusError as e:
                raise Exception(
                    f"OpenRouter API error: {e.response.status_code} - {e.response.text}"
                )
            except httpx.RequestError as e:
                raise Exception(f"OpenRouter request failed: {str(e)}")
            except (KeyError, IndexError) as e:
                raise Exception(f"Unexpected OpenRouter response format: {str(e)}")


# Global instance
llm_client = OpenRouterClient()
