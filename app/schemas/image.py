from pydantic import BaseModel, Field
from typing import Optional

class ImageGenerateRequest(BaseModel):
    outfit_id: Optional[str] = Field(None, description="ID của outfit (nếu có)")
    prompt: Optional[str] = Field(None, description="Mô tả tùy chỉnh bằng văn bản")
    category: Optional[str] = Field("Truyền thống", description="Phân loại áo dài")
    color: Optional[str] = Field("Trắng", description="Màu sắc")
    fabric: Optional[str] = Field("Vải lụa", description="Chất liệu")
    pattern: Optional[str] = Field(None, description="Họa tiết")
    accessories: Optional[list[str]] = Field(default_factory=list, description="Phụ kiện")
    gender: Optional[str] = Field("female", description="Giới tính người mặc (female / male)")
    background: Optional[str] = Field("studio", description="Bối cảnh chụp ảnh (Hoàng Thành Huế, Phố cổ Hội An, Studio...)")

class ImageGenerateResponse(BaseModel):
    image_url: str
    prompt_used: str
    outfit_id: Optional[str] = None

class TryOnRequest(BaseModel):
    upload_id: str = Field(..., description="ID của ảnh avatar đã tải lên")
    outfit_id: str = Field(..., description="ID của outfit cần thử")

class TryOnResponse(BaseModel):
    result_image_url: str
    original_image_url: str
    outfit_applied: str
    ai_notes: Optional[str] = None
