from beanie import Document
from datetime import datetime, timezone
from typing import Optional, Dict, Any

class Upload(Document):
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    upload_type: str  # "avatar" | "reference"
    ai_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "uploads"
