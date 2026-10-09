import logging
from typing import Dict, Any, Optional
from app.schemas.image import ImageGenerateRequest, TryOnRequest
from app.services.outfit_service import get_outfit
from app.services.upload_service import get_upload
from app.ai.image_gen import generate_outfit_image

logger = logging.getLogger("vietphuc.image_service")

async def generate_image_custom(req: ImageGenerateRequest) -> Dict[str, Any]:
    """Tạo hình ảnh outfit theo yêu cầu độc lập."""
    category = req.category or "Truyền thống"
    color = req.color or "Trắng"
    fabric = req.fabric or "Vải lụa"
    pattern = req.pattern
    accessories = req.accessories or []

    # Nếu có outfit_id, lấy thông tin chính xác từ outfit
    if req.outfit_id:
        outfit = await get_outfit(req.outfit_id)
        if outfit:
            category = outfit["category"]
            color = outfit["color"]
            fabric = outfit["fabric"]
            pattern = outfit.get("pattern")
            accessories = outfit.get("accessories", [])

    image_url = await generate_outfit_image(
        category=category,
        color=color,
        fabric=fabric,
        pattern=pattern,
        accessories=accessories,
        gender=req.gender or "female",
        background=req.background or "Không gian kiến trúc Việt Nam cổ kính",
        subdir="generated",
    )

    prompt_summary = f"Ảnh chụp thời trang áo dài {category}, màu {color}, chất liệu {fabric}, bối cảnh {req.background}"

    return {
        "image_url": image_url or "/static/uploads/default_placeholder.jpg",
        "prompt_used": prompt_summary,
        "outfit_id": req.outfit_id,
    }

async def try_on_outfit(req: TryOnRequest) -> Dict[str, Any]:
    """Mô phỏng thử đồ trên avatar người dùng."""
    upload = await get_upload(req.upload_id)
    outfit = await get_outfit(req.outfit_id)

    if not upload or not outfit:
        raise ValueError("Không tìm thấy ảnh người dùng hoặc outfit chỉ định.")

    gender = "male" if "Nam" in outfit["category"] else "female"
    result_image_url = await generate_outfit_image(
        category=outfit["category"],
        color=outfit["color"],
        fabric=outfit["fabric"],
        pattern=outfit.get("pattern"),
        accessories=outfit.get("accessories", []),
        gender=gender,
        background="Studio chụp hình chân dung nghệ thuật",
        subdir="tryon",
    )

    return {
        "result_image_url": result_image_url or upload["file_url"],
        "original_image_url": upload["file_url"],
        "outfit_applied": outfit["name"],
        "ai_notes": f"Trang phục {outfit['name']} đã được mô phỏng phù hợp với tỷ lệ và phong cách của bạn.",
    }
