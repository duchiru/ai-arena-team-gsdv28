from beanie import Document
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

class Outfit(Document):
    name: str
    category: str
    occasion: str
    color: str
    fabric: str
    pattern_technique: Optional[str] = None
    pattern: Optional[str] = None
    accessories: List[str] = []
    structural_features: List[str] = []
    warnings: List[Dict[str, Any]] = []
    cultural_info: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "outfits"
