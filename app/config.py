from pydantic import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "DEV"
    DATABASE_URL: str = "sqlite:///./webchat.db"
    TEST_DATABASE_URL: str = "sqlite:///./testing-webchat.db"
    ADMIN_USERNAME: str = "neo"
    ADMIN_PASSWORD: str = "ChangeItn0w!"
    JWT_SECRET: str = "J0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9eo"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
