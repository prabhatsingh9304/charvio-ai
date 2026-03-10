from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Database
    DATABASE_URL: str
    
    # LLM
    LLM_API_KEY: str
    LLM_MODEL: str
    LLM_BASE_URL: str
    
    # Application
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # Token Budget
    MAX_CONTEXT_TOKENS: int = 100000
    MAX_RESPONSE_TOKENS: int = 4000
    HISTORY_TRUNCATE_THRESHOLD: int = 80000

    # AWS
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    AWS_BUCKET_NAME: Optional[str] = None

    # Auth
    SECRET_KEY: str = "your-secret-key-here"  # Default for dev only
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google OAuth
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
