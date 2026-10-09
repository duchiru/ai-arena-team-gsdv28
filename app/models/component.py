from beanie import Document
from typing import Literal, Optional

ComponentType = Literal[
    "occasion",
    "color",
    "fabric",
    "pattern_technique",
    "pattern",
    "accessory",
    "structural_feature",
]

class Component(Document):
    type: str  # occasion, color, fabric, pattern_technique, pattern, accessory, structural_feature
    name: str
    description: str
    hex_code: Optional[str] = None  # Dành cho màu sắc
    image_url: Optional[str] = None

    class Settings:
        name = "components"
        indexes = ["type", "name"]
