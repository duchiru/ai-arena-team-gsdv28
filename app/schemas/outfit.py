from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class OutfitCreate(BaseModel):
    category: str = Field(..., description="Phân loại trang phục (ví dụ: Truyền thống, Cách tân - Nữ)")
    occasion: str = Field(..., description="Bối cảnh (ví dụ: Lễ nghi, Sự kiện, Học đường)")
    color: str = Field(..., description="Màu sắc chính (ví dụ: Trắng, Xanh lam, Đỏ)")
    fabric: str = Field(..., description="Chất liệu (ví dụ: Vải lụa, Vải gấm)")
    pattern_technique: Optional[str] = Field(None, description="Phương pháp tạo họa tiết")
    pattern: Optional[str] = Field(None, description="Họa tiết")
    accessories: List[str] = Field(default_factory=list, description="Danh sách phụ kiện")
    custom_name: Optional[str] = Field(None, description="Tên tùy chỉnh cho outfit")
    generate_image: bool = Field(False, description="Tự động sinh ảnh AI ngay khi tạo")

class OutfitResponse(BaseModel):
    id: str
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
    created_at: datetime

class OutfitListResponse(BaseModel):
    items: List[OutfitResponse]
    total: int
