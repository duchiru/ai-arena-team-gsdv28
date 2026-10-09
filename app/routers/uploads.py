from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.upload import UploadResponse
from app.services.upload_service import handle_upload, get_upload, delete_upload

router = APIRouter(prefix="/uploads", tags=["7. Tải ảnh & Phân tích Vision (Uploads)"])

@router.post("/", response_model=UploadResponse, summary="Tải lên ảnh chân dung / avatar và phân tích qua Gemini Vision")
async def upload_file_endpoint(
    file: UploadFile = File(..., description="Tệp ảnh (jpg, png, webp, tối đa 10MB)"),
    upload_type: str = Form("avatar", description="Loại ảnh: avatar hoặc reference"),
):
    return await handle_upload(file=file, upload_type=upload_type)

@router.get("/{upload_id}", response_model=UploadResponse, summary="Lấy thông tin và phân tích của tệp đã tải lên")
async def get_upload_detail(upload_id: str):
    item = await get_upload(upload_id)
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy tệp tải lên này.")
    return item

@router.delete("/{upload_id}", summary="Xóa tệp đã tải lên")
async def delete_upload_endpoint(upload_id: str):
    success = await delete_upload(upload_id)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy tệp để xóa.")
    return {"message": "Đã xóa tệp thành công."}
