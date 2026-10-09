from pydantic import BaseModel, Field
from typing import List, Optional

class ValidateRequest(BaseModel):
    category: Optional[str] = Field(None, description="Tên phân loại (Truyền thống, Cách tân - Nữ, Cách tân - Nam)")
    occasion: Optional[str] = Field(None, description="Bối cảnh sử dụng")
    color: Optional[str] = Field(None, description="Màu sắc")
    fabric: Optional[str] = Field(None, description="Chất liệu vải")
    pattern_technique: Optional[str] = Field(None, description="Phương pháp tạo họa tiết")
    pattern: Optional[str] = Field(None, description="Họa tiết")
    accessories: List[str] = Field(default_factory=list, description="Danh sách phụ kiện")

class WarningDetail(BaseModel):
    severity: str = "warning"
    components: List[str]
    reason: str

class ValidateResponse(BaseModel):
    is_valid: bool
    warnings: List[WarningDetail]
    suggestions: List[str] = Field(default_factory=list)
