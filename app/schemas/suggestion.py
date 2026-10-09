from pydantic import BaseModel, Field
from typing import List, Optional

class SuggestRequest(BaseModel):
    prompt: str = Field(..., description="Yêu cầu hoặc bối cảnh bằng ngôn ngữ tự nhiên")
    gender: Optional[str] = Field("female", description="Giới tính (female / male)")

class SuggestOccasionRequest(BaseModel):
    occasion: str = Field(..., description="Bối cảnh (Dự tiệc, Lễ nghi, Học đường, Công sở...)")
    weather: Optional[str] = Field("mát mẻ", description="Thời tiết (nóng, lạnh, mát mẻ, mưa...)")
    gender: Optional[str] = Field("female", description="Giới tính (female / male)")

class ColorHarmonyRequest(BaseModel):
    colors: List[str] = Field(..., description="Danh sách màu sắc cần kiểm tra độ hài hòa")
    category: Optional[str] = Field("Truyền thống", description="Phân loại áo dài")

class CompareRequest(BaseModel):
    outfit_ids: List[str] = Field(..., min_length=2, max_length=5, description="Danh sách 2-5 ID outfit cần so sánh")

class OutfitSuggestionItem(BaseModel):
    category: str
    occasion: str
    color: str
    fabric: str
    pattern_technique: Optional[str] = None
    pattern: Optional[str] = None
    accessories: List[str] = Field(default_factory=list)
    reason: str
    cultural_note: Optional[str] = None
    image_url: Optional[str] = None

class SuggestResponse(BaseModel):
    suggestions: List[OutfitSuggestionItem]
    ai_note: Optional[str] = None

class ColorHarmonyResponse(BaseModel):
    is_harmonious: bool
    score: int
    explanation: str
    alternatives: List[str] = Field(default_factory=list)

class CompareResponse(BaseModel):
    outfits: List[dict]
    formality_ranking: List[str]
    cultural_authenticity: List[str]
    versatility: List[str]
    ai_analysis: str
