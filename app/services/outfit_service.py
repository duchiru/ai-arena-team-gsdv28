import uuid
import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from beanie import PydanticObjectId
from app.models.outfit import Outfit
from app.schemas.outfit import OutfitCreate, OutfitResponse
from app.services.validation_service import validate_combination
from app.services.component_service import get_category_by_id
from app.ai.client import ai_client
from app.ai.prompts import CULTURAL_INFO_PROMPT
from app.ai.image_gen import generate_outfit_image
from app.database import is_connected

logger = logging.getLogger("vietphuc.outfit_service")

# In-memory storage for offline demo
MEMORY_OUTFITS: Dict[str, Dict[str, Any]] = {}

async def create_outfit(data: OutfitCreate) -> Dict[str, Any]:
    """Tạo bộ phối đồ mới với kiểm tra văn hóa và tích hợp AI."""
    # 1. Kiểm tra văn hóa
    val_result = await validate_combination(
        category=data.category,
        occasion=data.occasion,
        color=data.color,
        fabric=data.fabric,
        pattern_technique=data.pattern_technique,
        pattern=data.pattern,
        accessories=data.accessories,
    )
    warnings = val_result.get("warnings", [])

    # 2. Tự động sinh tên trang phục nếu không có tên tùy chỉnh
    name = data.custom_name
    if not name:
        pat_part = f" {data.pattern}" if data.pattern else ""
        name = f"Áo dài {data.category} {data.fabric} {data.color}{pat_part}"

    # 3. Lấy structural features từ category
    cat_info = await get_category_by_id(data.category)
    structural_features = cat_info.get("structural_features", []) if cat_info else []

    # 4. Sinh thông tin ý nghĩa văn hóa bằng Gemini AI
    cultural_info = None
    try:
        acc_str = ", ".join(data.accessories) if data.accessories else "Không có"
        cultural_prompt = CULTURAL_INFO_PROMPT.format(
            category=data.category,
            occasion=data.occasion,
            color=data.color,
            fabric=data.fabric,
            pattern_technique=data.pattern_technique or "Tự nhiên",
            pattern=data.pattern or "Vải trơn",
            accessories=acc_str,
        )
        cultural_info = await ai_client.generate_text(cultural_prompt)
    except Exception as e:
        logger.warning(f"Không thể sinh cultural_info qua AI: {e}")
        cultural_info = f"Bộ trang phục {name} phù hợp cho bối cảnh {data.occasion}."

    # 5. Sinh hình ảnh bằng Imagen (nếu được yêu cầu)
    image_url = None
    if data.generate_image:
        try:
            gender = "male" if "Nam" in data.category else "female"
            image_url = await generate_outfit_image(
                category=data.category,
                color=data.color,
                fabric=data.fabric,
                pattern=data.pattern,
                accessories=data.accessories,
                gender=gender,
                background=f"Bối cảnh {data.occasion} tại Việt Nam",
            )
        except Exception as e:
            logger.warning(f"Lỗi sinh ảnh AI cho outfit: {e}")

    now = datetime.now(timezone.utc)
    
    # 6. Lưu vào MongoDB hoặc In-memory fallback
    if is_connected:
        try:
            doc = Outfit(
                name=name,
                category=data.category,
                occasion=data.occasion,
                color=data.color,
                fabric=data.fabric,
                pattern_technique=data.pattern_technique,
                pattern=data.pattern,
                accessories=data.accessories,
                structural_features=structural_features,
                warnings=warnings,
                cultural_info=cultural_info,
                image_url=image_url,
                created_at=now,
            )
            await doc.insert()
            return {
                "id": str(doc.id),
                "name": doc.name,
                "category": doc.category,
                "occasion": doc.occasion,
                "color": doc.color,
                "fabric": doc.fabric,
                "pattern_technique": doc.pattern_technique,
                "pattern": doc.pattern,
                "accessories": doc.accessories,
                "structural_features": doc.structural_features,
                "warnings": doc.warnings,
                "cultural_info": doc.cultural_info,
                "image_url": doc.image_url,
                "created_at": doc.created_at,
            }
        except Exception as e:
            logger.error(f"Lỗi lưu MongoDB: {e}")

    # Fallback lưu bộ nhớ RAM
    outfit_id = f"outfit_{uuid.uuid4().hex[:8]}"
    item = {
        "id": outfit_id,
        "name": name,
        "category": data.category,
        "occasion": data.occasion,
        "color": data.color,
        "fabric": data.fabric,
        "pattern_technique": data.pattern_technique,
        "pattern": data.pattern,
        "accessories": data.accessories,
        "structural_features": structural_features,
        "warnings": warnings,
        "cultural_info": cultural_info,
        "image_url": image_url,
        "created_at": now,
    }
    MEMORY_OUTFITS[outfit_id] = item
    return item

async def get_outfit(outfit_id: str) -> Optional[Dict[str, Any]]:
    """Lấy chi tiết outfit theo ID."""
    if is_connected:
        try:
            doc = await Outfit.get(PydanticObjectId(outfit_id))
            if doc:
                return {
                    "id": str(doc.id),
                    "name": doc.name,
                    "category": doc.category,
                    "occasion": doc.occasion,
                    "color": doc.color,
                    "fabric": doc.fabric,
                    "pattern_technique": doc.pattern_technique,
                    "pattern": doc.pattern,
                    "accessories": doc.accessories,
                    "structural_features": doc.structural_features,
                    "warnings": doc.warnings,
                    "cultural_info": doc.cultural_info,
                    "image_url": doc.image_url,
                    "created_at": doc.created_at,
                }
        except Exception:
            pass
    return MEMORY_OUTFITS.get(outfit_id)

async def list_outfits(skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
    """Lấy danh sách các outfit."""
    if is_connected:
        try:
            docs = await Outfit.find_all().skip(skip).limit(limit).to_list()
            return [
                {
                    "id": str(d.id),
                    "name": d.name,
                    "category": d.category,
                    "occasion": d.occasion,
                    "color": d.color,
                    "fabric": d.fabric,
                    "pattern_technique": d.pattern_technique,
                    "pattern": d.pattern,
                    "accessories": d.accessories,
                    "structural_features": d.structural_features,
                    "warnings": d.warnings,
                    "cultural_info": d.cultural_info,
                    "image_url": d.image_url,
                    "created_at": d.created_at,
                }
                for d in docs
            ]
        except Exception:
            pass
    return list(MEMORY_OUTFITS.values())[skip : skip + limit]

async def delete_outfit(outfit_id: str) -> bool:
    """Xóa outfit theo ID."""
    if is_connected:
        try:
            doc = await Outfit.get(PydanticObjectId(outfit_id))
            if doc:
                await doc.delete()
                return True
        except Exception:
            pass
    if outfit_id in MEMORY_OUTFITS:
        del MEMORY_OUTFITS[outfit_id]
        return True
    return False

async def regenerate_image(outfit_id: str) -> Optional[str]:
    """Sinh lại ảnh AI cho một outfit đã có."""
    outfit = await get_outfit(outfit_id)
    if not outfit:
        return None
    
    gender = "male" if "Nam" in outfit["category"] else "female"
    image_url = await generate_outfit_image(
        category=outfit["category"],
        color=outfit["color"],
        fabric=outfit["fabric"],
        pattern=outfit.get("pattern"),
        accessories=outfit.get("accessories", []),
        gender=gender,
        background=f"Bối cảnh {outfit['occasion']} tại Việt Nam",
    )
    
    if image_url:
        outfit["image_url"] = image_url
        if is_connected:
            try:
                doc = await Outfit.get(PydanticObjectId(outfit_id))
                if doc:
                    doc.image_url = image_url
                    await doc.save()
            except Exception:
                pass
    return image_url
