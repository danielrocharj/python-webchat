from pydantic import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "dev"
    DATABASE_URL: str = "sqlite:///./webchat.db"
    TEST_DATABASE_URL: str = "sqlite:///./testing-webchat.db"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()