"""환경 변수 및 애플리케이션 설정"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """애플리케이션 설정 클래스"""
    
    # OpenAI 설정
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4.1-nano"  # 기본 모델 (가장 빠르고 저렴)
    
    # Firebase 설정
    FIREBASE_PROJECT_ID: str = "cardnews-dev"
    FIREBASE_PRIVATE_KEY_PATH: str = "./serviceAccountKey.json"
    
    # Backend 설정
    BACKEND_PORT: int = 8000
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # 제한
    MAX_TEXT_LENGTH: int = 10000
    RATE_LIMIT_PER_MINUTE: int = 10
    
    # Debug
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """CORS 허용 오리진 리스트"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(',')]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 전역 설정 인스턴스
settings = Settings()

