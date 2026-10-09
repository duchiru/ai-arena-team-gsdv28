from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.lookbook import (
    LookbookCreate,
    LookbookResponse,
    LookbookListResponse,
)
from app.services.lookbook_service import (
    create_lookbook,
    get_lookbook_by_id,
    get_lookbook_by_share_code,
    list_lookbooks,
    add_outfit_to_lookbook,
    remove_outfit_from_lookbook,
    delete_lookbook,
)

router = APIRouter(prefix="/lookbooks", tags=["8. Bộ sưu tập Lookbook & Chia sẻ (Lookbooks)"])

@router.post("/", response_model=LookbookResponse, status_code=status.HTTP_201_CREATED, summary="Tạo Lookbook mới")
async def create_new_lookbook(data: LookbookCreate):
    return await create_lookbook(data)

@router.get("/", response_model=LookbookListResponse, summary="Danh sách Lookbooks")
async def get_all_lookbooks(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    items = await list_lookbooks(skip=skip, limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/shared/{share_code}", response_model=LookbookResponse, summary="Xem Lookbook qua mã chia sẻ công khai")
async def view_shared_lookbook(share_code: str):
    item = await get_lookbook_by_share_code(share_code)
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy Lookbook với mã chia sẻ này.")
    return item

@router.get("/{lookbook_id}", response_model=LookbookResponse, summary="Chi tiết Lookbook")
async def get_lookbook_detail(lookbook_id: str):
    item = await get_lookbook_by_id(lookbook_id)
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy Lookbook.")
    return item

@router.post("/{lookbook_id}/outfits", response_model=LookbookResponse, summary="Thêm outfit vào Lookbook")
async def add_outfit(lookbook_id: str, outfit_id: str = Query(..., description="ID của outfit cần thêm")):
    updated = await add_outfit_to_lookbook(lookbook_id, outfit_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy Lookbook.")
    return updated

@router.delete("/{lookbook_id}/outfits/{outfit_id}", response_model=LookbookResponse, summary="Gỡ outfit khỏi Lookbook")
async def remove_outfit(lookbook_id: str, outfit_id: str):
    updated = await remove_outfit_from_lookbook(lookbook_id, outfit_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy Lookbook.")
    return updated

@router.delete("/{lookbook_id}", summary="Xóa Lookbook")
async def delete_lookbook_endpoint(lookbook_id: str):
    success = await delete_lookbook(lookbook_id)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy Lookbook để xóa.")
    return {"message": "Đã xóa Lookbook thành công."}
