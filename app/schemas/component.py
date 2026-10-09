from pydantic import BaseModel
from typing import List, Optional

class ComponentResponse(BaseModel):
    id: str
    type: str
    name: str
    description: str
    hex_code: Optional[str] = None
    image_url: Optional[str] = None

class ComponentListResponse(BaseModel):
    items: List[ComponentResponse]
    total: int

class CategoryResponse(BaseModel):
    id: str
    name: str
    description: str
    occasions: List[str]
    colors: List[str]
    fabrics: List[str]
    pattern_techniques: List[str]
    patterns: List[str]
    accessories: List[str]
    structural_features: List[str]

class CategoryListResponse(BaseModel):
    items: List[CategoryResponse]
    total: int
