from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.outfit import OutfitResponse

class LookbookCreate(BaseModel):
    title: str = Field(..., description="Tiêu đề lookbook")
    description: Optional[str] = Field(None, description="Mô tả lookbook")
    outfit_ids: List[str] = Field(default_factory=list, description="Danh sách ID outfit ban đầu")

class LookbookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class LookbookResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    share_code: str
    outfit_ids: List[str]
    outfits: List[OutfitResponse] = []
    created_at: datetime

class LookbookListResponse(BaseModel):
    items: List[LookbookResponse]
    total: int
