from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "prod"
    SYSTEM_STATUS: str = "ACTIVE"
    MONGODB_URI: str = "mongodb://localhost:27017"
    JWT_SECRET: str = "change-me"
    BACKEND_CORS_ORIGINS: str = "*"

    CASHFREE_CLIENT_ID: str | None = None
    CASHFREE_CLIENT_SECRET: str | None = None
    RAZORPAY_KEY_ID: str | None = None
    RAZORPAY_KEY_SECRET: str | None = None


settings = Settings()
