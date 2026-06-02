from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Field annotations must match the keys in your .env file EXACTLY
    GROQ_API_KEY: str
    test_open_api_key: str
    test_database_url: str
    test_debug: bool

   class Config:
        env_file = ".env"
settings = Settings()
