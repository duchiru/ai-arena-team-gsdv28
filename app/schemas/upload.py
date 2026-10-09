from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class UploadResponse(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_url: str
    file_size: int
    mime_type: str
    upload_type: str
    ai_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime
