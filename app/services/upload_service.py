import os
import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from PIL import Image
from fastapi import UploadFile, HTTPException
from beanie import PydanticObjectId
from app.config import settings
from app.models.upload import Upload
from app.ai.client import ai_client
from app.ai.prompts import ANALYZE_UPLOAD_PROMPT
from app.database import is_connected

logger = logging.getLogger("vietphuc.upload_service")

MEMORY_UPLOADS: Dict[str, Dict[str, Any]] = {}

MAX_DIMENSION = 2048

async def handle_upload(file: UploadFile, upload_type: str = "avatar") -> Dict[str, Any]:
    """Xử lý tải lên hình ảnh, nén ảnh và phân tích AI qua Gemini Vision."""
    # 1. Kiểm tra phần mở rộng
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Định dạng tệp {ext} không được hỗ trợ. Chỉ chấp nhận {', '.join(settings.ALLOWED_EXTENSIONS)}."
        )

    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="Dung lượng tệp vượt quá giới hạn 10MB.")

    # 2. Tạo đường dẫn lưu trữ
    filename = f"{upload_type}_{uuid.uuid4().hex[:12]}{ext}"
    subdir = "users"
    dir_path = os.path.join(settings.UPLOAD_DIR, subdir)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, filename)

    with open(file_path, "wb") as f:
        f.write(content)

    # 3. Nén ảnh nếu kích thước quá lớn
    try:
        with Image.open(file_path) as img:
            if max(img.size) > MAX_DIMENSION:
                img.thumbnail((MAX_DIMENSION, MAX_DIMENSION))
                img.save(file_path)
    except Exception as e:
        logger.warning(f"Lỗi khi xử lý resize ảnh: {e}")

    # 4. Phân tích ảnh bằng Gemini Vision
    ai_analysis = None
    try:
        mime = file.content_type or "image/jpeg"
        ai_analysis = await ai_client.analyze_image(
            image_bytes=content,
            mime_type=mime,
            prompt=ANALYZE_UPLOAD_PROMPT,
        )
    except Exception as e:
        logger.warning(f"Lỗi phân tích Gemini Vision: {e}")
        ai_analysis = {
            "detected_garment": "Hình ảnh người dùng tải lên",
            "detected_colors": ["Tự nhiên"],
            "body_type_suggestion": "Phom dáng áo dài truyền thống ôm vừa vặn sẽ rất tôn dáng.",
            "suggestions": ["Thử phối cùng phụ kiện trâm cài hoặc kiềng cổ."]
        }

    now = datetime.now(timezone.utc)
    file_url = f"/static/uploads/{subdir}/{filename}"

    # 5. Lưu thông tin vào DB / RAM
    if is_connected:
        try:
            doc = Upload(
                filename=filename,
                original_filename=file.filename or "unknown",
                file_path=file_url,
                file_size=len(content),
                mime_type=file.content_type or "image/jpeg",
                upload_type=upload_type,
                ai_analysis=ai_analysis,
                created_at=now,
            )
            await doc.insert()
            return {
                "id": str(doc.id),
                "filename": doc.filename,
                "original_filename": doc.original_filename,
                "file_url": doc.file_path,
                "file_size": doc.file_size,
                "mime_type": doc.mime_type,
                "upload_type": doc.upload_type,
                "ai_analysis": doc.ai_analysis,
                "created_at": doc.created_at,
            }
        except Exception as e:
            logger.error(f"Lỗi lưu Upload vào MongoDB: {e}")

    upload_id = f"up_{uuid.uuid4().hex[:8]}"
    item = {
        "id": upload_id,
        "filename": filename,
        "original_filename": file.filename or "unknown",
        "file_url": file_url,
        "file_size": len(content),
        "mime_type": file.content_type or "image/jpeg",
        "upload_type": upload_type,
        "ai_analysis": ai_analysis,
        "created_at": now,
    }
    MEMORY_UPLOADS[upload_id] = item
    return item

async def get_upload(upload_id: str) -> Optional[Dict[str, Any]]:
    """Lấy thông tin tệp tải lên."""
    if is_connected:
        try:
            doc = await Upload.get(PydanticObjectId(upload_id))
            if doc:
                return {
                    "id": str(doc.id),
                    "filename": doc.filename,
                    "original_filename": doc.original_filename,
                    "file_url": doc.file_path,
                    "file_size": doc.file_size,
                    "mime_type": doc.mime_type,
                    "upload_type": doc.upload_type,
                    "ai_analysis": doc.ai_analysis,
                    "created_at": doc.created_at,
                }
        except Exception:
            pass
    return MEMORY_UPLOADS.get(upload_id)

async def delete_upload(upload_id: str) -> bool:
    """Xóa tệp tải lên và tệp trên đĩa."""
    up = await get_upload(upload_id)
    if not up:
        return False
    
    # Xóa file vật lý
    try:
        rel_path = up["file_url"].replace("/static/uploads/", "")
        disk_path = os.path.join(settings.UPLOAD_DIR, rel_path)
        if os.path.exists(disk_path):
            os.remove(disk_path)
    except Exception as e:
        logger.warning(f"Lỗi xóa file vật lý: {e}")

    if is_connected:
        try:
            doc = await Upload.get(PydanticObjectId(upload_id))
            if doc:
                await doc.delete()
                return True
        except Exception:
            pass
    if upload_id in MEMORY_UPLOADS:
        del MEMORY_UPLOADS[upload_id]
        return True
    return False
