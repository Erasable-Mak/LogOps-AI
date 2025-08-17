from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    openrouter_api_key: str
    data_dir: str = "./data"
    openrouter_model: str = "deepseek-ai/deepseek-coder-1.3b-instruct"

    class Config:
        env_file = ".env"

settings = Settings()

