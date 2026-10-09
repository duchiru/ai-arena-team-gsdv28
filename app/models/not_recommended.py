from beanie import Document
from typing import List

class NotRecommended(Document):
    components: List[str]
    reason: str

    class Settings:
        name = "not_recommended"
