import uuid
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from beanie import PydanticObjectId
from app.models.lookbook import Lookbook
from app.schemas.lookbook import LookbookCreate, LookbookUpdate
from app.services.outfit_service import get_outfit
from app.database import is_connected

logger = logging.getLogger("vietphuc.lookbook_service")

MEMORY_LOOKBOOKS: Dict[str, Dict[str, Any]] = {}

async def create_lookbook(data: LookbookCreate) -> Dict[str, Any]:
    """Tạo lookbook mới với mã chia sẻ duy nhất."""
    share_code = f"vp-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc)
    
    if is_connected:
        try:
            oid_list = []
            for oid in data.outfit_ids:
                try:
                    oid_list.append(PydanticObjectId(oid))
                except Exception:
                    pass
            doc = Lookbook(
                title=data.title,
                description=data.description,
                share_code=share_code,
                outfit_ids=oid_list,
                created_at=now,
            )
            await doc.insert()
            return await populate_lookbook_details({
                "id": str(doc.id),
                "title": doc.title,
                "description": doc.description,
                "share_code": doc.share_code,
                "outfit_ids": [str(x) for x in doc.outfit_ids],
                "created_at": doc.created_at,
            })
        except Exception as e:
            logger.error(f"Lỗi tạo Lookbook trong MongoDB: {e}")

    lb_id = f"lb_{uuid.uuid4().hex[:8]}"
    item = {
        "id": lb_id,
        "title": data.title,
        "description": data.description,
        "share_code": share_code,
        "outfit_ids": data.outfit_ids,
        "created_at": now,
    }
    MEMORY_LOOKBOOKS[lb_id] = item
    return await populate_lookbook_details(item)

async def populate_lookbook_details(lb: Dict[str, Any]) -> Dict[str, Any]:
    """Bổ sung danh sách thông tin outfit đầy đủ cho lookbook."""
    outfits = []
    for oid in lb.get("outfit_ids", []):
        o = await get_outfit(oid)
        if o:
            outfits.append(o)
    result = dict(lb)
    result["outfits"] = outfits
    return result

async def get_lookbook_by_id(lb_id: str) -> Optional[Dict[str, Any]]:
    """Lấy lookbook theo ID."""
    if is_connected:
        try:
            doc = await Lookbook.get(PydanticObjectId(lb_id))
            if doc:
                return await populate_lookbook_details({
                    "id": str(doc.id),
                    "title": doc.title,
                    "description": doc.description,
                    "share_code": doc.share_code,
                    "outfit_ids": [str(x) for x in doc.outfit_ids],
                    "created_at": doc.created_at,
                })
        except Exception:
            pass
    item = MEMORY_LOOKBOOKS.get(lb_id)
    if item:
        return await populate_lookbook_details(item)
    return None

async def get_lookbook_by_share_code(code: str) -> Optional[Dict[str, Any]]:
    """Lấy lookbook qua mã chia sẻ công khai."""
    if is_connected:
        try:
            doc = await Lookbook.find_one(Lookbook.share_code == code)
            if doc:
                return await populate_lookbook_details({
                    "id": str(doc.id),
                    "title": doc.title,
                    "description": doc.description,
                    "share_code": doc.share_code,
                    "outfit_ids": [str(x) for x in doc.outfit_ids],
                    "created_at": doc.created_at,
                })
        except Exception:
            pass
    for item in MEMORY_LOOKBOOKS.values():
        if item["share_code"] == code:
            return await populate_lookbook_details(item)
    return None

async def list_lookbooks(skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
    """Danh sách lookbooks."""
    if is_connected:
        try:
            docs = await Lookbook.find_all().skip(skip).limit(limit).to_list()
            res = []
            for d in docs:
                item = await populate_lookbook_details({
                    "id": str(d.id),
                    "title": d.title,
                    "description": d.description,
                    "share_code": d.share_code,
                    "outfit_ids": [str(x) for x in d.outfit_ids],
                    "created_at": d.created_at,
                })
                res.append(item)
            return res
        except Exception:
            pass
    res = []
    items = list(MEMORY_LOOKBOOKS.values())[skip : skip + limit]
    for it in items:
        res.append(await populate_lookbook_details(it))
    return res

async def add_outfit_to_lookbook(lb_id: str, outfit_id: str) -> Optional[Dict[str, Any]]:
    """Thêm outfit vào lookbook."""
    lb = await get_lookbook_by_id(lb_id)
    if not lb:
        return None
    if outfit_id not in lb["outfit_ids"]:
        lb["outfit_ids"].append(outfit_id)
        if is_connected:
            try:
                doc = await Lookbook.get(PydanticObjectId(lb_id))
                if doc:
                    doc.outfit_ids.append(PydanticObjectId(outfit_id))
                    await doc.save()
            except Exception:
                pass
    return await populate_lookbook_details(lb)

async def remove_outfit_from_lookbook(lb_id: str, outfit_id: str) -> Optional[Dict[str, Any]]:
    """Xóa outfit khỏi lookbook."""
    lb = await get_lookbook_by_id(lb_id)
    if not lb:
        return None
    if outfit_id in lb["outfit_ids"]:
        lb["outfit_ids"].remove(outfit_id)
        if is_connected:
            try:
                doc = await Lookbook.get(PydanticObjectId(lb_id))
                if doc:
                    doc.outfit_ids = [x for x in doc.outfit_ids if str(x) != outfit_id]
                    await doc.save()
            except Exception:
                pass
    return await populate_lookbook_details(lb)

async def delete_lookbook(lb_id: str) -> bool:
    """Xóa lookbook."""
    if is_connected:
        try:
            doc = await Lookbook.get(PydanticObjectId(lb_id))
            if doc:
                await doc.delete()
                return True
        except Exception:
            pass
    if lb_id in MEMORY_LOOKBOOKS:
        del MEMORY_LOOKBOOKS[lb_id]
        return True
    return False
