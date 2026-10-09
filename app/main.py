import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import connect_db, close_db, is_connected
from app.routers import all_routers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("vietphuc.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi tạo thư mục uploads
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "outfits"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "generated"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "tryon"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "users"), exist_ok=True)

    # Kết nối MongoDB
    await connect_db()
    yield
    # Đóng kết nối MongoDB
    await close_db()

app = FastAPI(
    title="Việt Phục Remix API",
    description="""
# Hệ thống REST API Backend — Việt Phục Remix
Nền tảng khám phá, phối đồ và tìm hiểu giá trị văn hóa trang phục truyền thống Việt Nam.

### Tính năng chính:
- **Khám phá & Tra cứu**: Phân loại áo dài (Truyền thống, Cách tân Nữ, Cách tân Nam), màu sắc, chất liệu, hoa văn, phụ kiện.
- **Cultural Validation Engine**: Tự động phát hiện và cảnh báo các phối hợp vi phạm quy chuẩn văn hóa dựa trên 16 quy tắc cốt lõi.
- **Gemini AI Assistant**: Gợi ý phối đồ qua ngôn ngữ tự nhiên, phân tích hài hòa màu sắc Á Đông, so sánh trang phục.
- **Imagen 4.0 Studio**: Tạo hình ảnh mô phỏng trang phục chân thực và thử đồ ảo qua avatar.
- **Lookbook & Sharing**: Lưu trữ bộ sưu tập và chia sẻ với mã liên kết công khai.
    """,
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware cho frontend kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Phục vụ thư mục tệp tĩnh (hình ảnh tải lên & ảnh AI tạo)
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/static/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Đăng ký toàn bộ các API Routers
for router in all_routers:
    app.include_router(router, prefix=settings.API_V1_PREFIX)

@app.get("/", tags=["Trang chủ"])
async def root():
    return {
        "app": "Việt Phục Remix API",
        "version": "2.0.0",
        "status": "online",
        "database_connected": is_connected,
        "docs_url": "/docs",
        "api_v1": settings.API_V1_PREFIX,
    }
