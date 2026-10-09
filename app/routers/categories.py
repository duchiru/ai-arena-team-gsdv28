from fastapi import APIRouter, HTTPException
from app.schemas.component import CategoryListResponse, CategoryResponse
from app.services.component_service import get_all_categories, get_category_by_id

router = APIRouter(prefix="/categories", tags=["1. Phân loại trang phục (Categories)"])

@router.get("/", response_model=CategoryListResponse, summary="Lấy danh sách các phân loại trang phục")
async def list_categories():
    items = await get_all_categories()
    return {"items": items, "total": len(items)}

@router.get("/{category_id}", response_model=CategoryResponse, summary="Chi tiết phân loại trang phục")
async def get_category(category_id: str):
    cat = await get_category_by_id(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Không tìm thấy phân loại trang phục này.")
    return cat
