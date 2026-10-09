import os
import uuid
import logging
from typing import Optional, List
from app.config import settings
from app.ai.client import ai_client
from app.ai.prompts import GENERATE_IMAGE_PROMPT_TEMPLATE

logger = logging.getLogger("vietphuc.image_gen")

async def generate_outfit_image(
    category: str,
    color: str,
    fabric: str,
    pattern: Optional[str] = None,
    accessories: Optional[List[str]] = None,
    gender: str = "female",
    background: str = "Studio chụp ảnh nghệ thuật truyền thống",
    subdir: str = "outfits",
) -> Optional[str]:
    """Sinh ảnh phối đồ bằng Imagen và lưu vào thư mục static."""
    person_type = "woman" if gender.lower() in ["female", "nữ"] else "man"
    acc_text = ", ".join(accessories) if accessories else "không có phụ kiện cầu kỳ"
    pat_text = pattern if pattern else "vải trơn thanh lịch"

    prompt = GENERATE_IMAGE_PROMPT_TEMPLATE.format(
        person_type=person_type,
        category=category,
        color=color,
        fabric=fabric,
        pattern=pat_text,
        accessories=acc_text,
        background=background,
    )

    image_bytes = await ai_client.generate_image(prompt)
    if not image_bytes:
        logger.warning("Không nhận được dữ liệu ảnh từ AI Imagen.")
        return None

    filename = f"{uuid.uuid4().hex[:12]}.jpg"
    target_dir = os.path.join(settings.UPLOAD_DIR, subdir)
    os.makedirs(target_dir, exist_ok=True)
    
    file_path = os.path.join(target_dir, filename)
    with open(file_path, "wb") as f:
        f.write(image_bytes)

    return f"/static/uploads/{subdir}/{filename}"
