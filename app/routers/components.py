from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.schemas.component import ComponentListResponse, ComponentResponse
from app.services.component_service import get_components, get_component_by_id

router = APIRouter(prefix="/components", tags=["2. Tra cứu thành phần (Components)"])

@router.get("/", response_model=ComponentListResponse, summary="Tra cứu danh sách thành phần trang phục")
async def list_components(
    type: Optional[str] = Query(None, description="Lọc theo loại: occasion, color, fabric, pattern_technique, pattern, accessory, structural_feature"),
    category: Optional[str] = Query(None, description="Lọc thành phần thuộc phân loại: Truyền thống, Cách tân - Nữ, Cách tân - Nam"),
):
    items = await get_components(type_filter=type, category_filter=category)
    return {"items": items, "total": len(items)}

@router.get("/{component_id}", response_model=ComponentResponse, summary="Chi tiết ý nghĩa một thành phần")
async def get_component(component_id: str):
    comp = await get_component_by_id(component_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Không tìm thấy thành phần này.")
    return comp
