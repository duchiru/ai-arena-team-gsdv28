import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Cấu hình kết nối MongoDB
    MONGODB_HOST: str = ""
    MONGODB_PORT: int = 27017
    MONGODB_USERNAME: str = ""
    MONGODB_PASSWORD: str = ""
    MONGODB_NAME: str = "vietphuc_remix"

    @property
    def MONGODB_URL(self) -> str:
        """Tự động xây dựng connection string dựa trên các thông số."""
        if not self.MONGODB_HOST:
            # Fallback nếu chưa điền host
            return f"mongodb://localhost:{self.MONGODB_PORT}/{self.MONGODB_NAME}"

        if self.MONGODB_USERNAME and self.MONGODB_PASSWORD:
            # Kết nối Atlas SRV hoặc authenticated Mongo
            if "." in self.MONGODB_HOST and not ":" in self.MONGODB_HOST:
                return (
                    f"mongodb+srv://{self.MONGODB_USERNAME}:{self.MONGODB_PASSWORD}"
                    f"@{self.MONGODB_HOST}/{self.MONGODB_NAME}"
                    f"?retryWrites=true&w=majority"
                )
            return (
                f"mongodb://{self.MONGODB_USERNAME}:{self.MONGODB_PASSWORD}"
                f"@{self.MONGODB_HOST}:{self.MONGODB_PORT}/{self.MONGODB_NAME}"
            )
        return f"mongodb://{self.MONGODB_HOST}:{self.MONGODB_PORT}/{self.MONGODB_NAME}"

    # Cấu hình Gemini AI
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-flash-latest"
    IMAGEN_MODEL: str = "imagen-4.0-generate-001"

    # Cấu hình Tải tệp (File Upload)
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list[str] = [".jpg", ".jpeg", ".png", ".webp"]

    # Cấu hình API
    API_V1_PREFIX: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
