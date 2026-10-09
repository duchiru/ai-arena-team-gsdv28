import logging
from pymongo import AsyncMongoClient
from beanie import init_beanie
from app.config import settings
from app.models import (
    GarmentType,
    Category,
    Component,
    NotRecommended,
    Outfit,
    Lookbook,
    Upload,
)

logger = logging.getLogger("vietphuc.database")

client: AsyncMongoClient | None = None
is_connected: bool = False

async def connect_db():
    global client, is_connected
    try:
        mongo_url = settings.MONGODB_URL
        logger.info(f"Đang kết nối MongoDB: {settings.MONGODB_HOST or 'localhost'}:{settings.MONGODB_PORT}")
        client = AsyncMongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        
        # Test ping to check if MongoDB is alive
        await client.admin.command('ping')
        
        await init_beanie(
            database=client[settings.MONGODB_NAME],
            document_models=[
                GarmentType,
                Category,
                Component,
                NotRecommended,
                Outfit,
                Lookbook,
                Upload,
            ],
        )
        is_connected = True
        logger.info("✅ Kết nối MongoDB và khởi tạo Beanie ODM thành công!")
    except Exception as e:
        is_connected = False
        logger.warning(
            f"⚠️ Không thể kết nối MongoDB ({e}). "
            f"Vui lòng kiểm tra thông tin cấu hình trong file .env hoặc đảm bảo MongoDB đang chạy."
        )

async def close_db():
    global client, is_connected
    if client:
        client.close()
        is_connected = False
        logger.info("Đã đóng kết nối MongoDB.")
