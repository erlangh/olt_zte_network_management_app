from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "OLT ZTE C320 Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://olt_user:olt_password@localhost:5432/olt_management"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # OLT Settings
    DEFAULT_SNMP_VERSION: str = "2c"
    DEFAULT_SNMP_PORT: int = 161
    DEFAULT_TELNET_PORT: int = 23
    SNMP_TIMEOUT: int = 5
    TELNET_TIMEOUT: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
