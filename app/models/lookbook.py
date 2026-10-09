from beanie import Document, PydanticObjectId
from datetime import datetime, timezone
from typing import List, Optional

class Lookbook(Document):
    title: str
    description: Optional[str] = None
    share_code: str  # Mã chia sẻ unique
    outfit_ids: List[PydanticObjectId] = []
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "lookbooks"
        indexes = [[("share_code", 1)]]
