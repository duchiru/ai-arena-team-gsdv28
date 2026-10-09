from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.outfit import OutfitCreate, OutfitResponse, OutfitListResponse
from app.services.outfit_service import (
    create_outfit,
    get_outfit,
    list_outfits,
    delete_outfit,
    regenerate_image,
)

router = APIRouter(prefix="/outfits", tags=["4. Quản lý phối đồ (Outfit Builder)"])

@router.post("/", response_model=OutfitResponse, status_code=status.HTTP_201_CREATED, summary="Tạo bộ phối đồ mới")
async def create_new_outfit(data: OutfitCreate):
    return await create_outfit(data)

@router.get("/", response_model=OutfitListResponse, summary="Danh sách các bộ phối đồ đã lưu")
async def get_all_outfits(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    items = await list_outfits(skip=skip, limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/{outfit_id}", response_model=OutfitResponse, summary="Chi tiết một bộ phối đồ")
async def get_outfit_detail(outfit_id: str):
    item = await get_outfit(outfit_id)
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy bộ phối đồ này.")
    return item

@router.delete("/{outfit_id}", summary="Xóa bộ phối đồ")
async def delete_outfit_item(outfit_id: str):
    success = await delete_outfit(outfit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy bộ phối đồ để xóa.")
    return {"message": "Đã xóa bộ phối đồ thành công."}

@router.post("/{outfit_id}/generate-image", summary="Tạo hoặc sinh lại ảnh AI cho bộ phối đồ")
async def generate_image_for_outfit(outfit_id: str):
    image_url = await regenerate_image(outfit_id)
    if not image_url:
        raise HTTPException(status_code=400, detail="Không thể tạo ảnh cho bộ phối đồ này.")
    return {"outfit_id": outfit_id, "image_url": image_url}
