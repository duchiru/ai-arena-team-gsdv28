from beanie import Document
from typing import List

class GarmentType(Document):
    name: str
    description: str

    class Settings:
        name = "garment_types"

class Category(Document):
    name: str
    description: str
    garment_type_id: str
    occasions: List[str] = []
    colors: List[str] = []
    fabrics: List[str] = []
    pattern_techniques: List[str] = []
    patterns: List[str] = []
    accessories: List[str] = []
    structural_features: List[str] = []

    class Settings:
        name = "categories"
