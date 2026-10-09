# Kế hoạch Thiết kế Hệ thống API Backend — Việt Phục Remix

## 1. Mô tả mục tiêu

Xây dựng hệ thống **REST API backend** cho ứng dụng **"Việt Phục Remix"** — nền tảng giúp học sinh, sinh viên khám phá, phối và tìm hiểu trang phục truyền thống Việt Nam (Áo dài truyền thống, Áo dài cách tân nữ, Áo dài cách tân nam). Hệ thống phục vụ dữ liệu trang phục, xử lý logic phối đồ, kiểm tra tính phù hợp văn hóa, tích hợp Gemini AI để gợi ý thông minh, **tạo hình ảnh trang phục bằng AI (Imagen 4.0)**, và **hỗ trợ tải lên ảnh/nhân vật đại diện để phân tích & thử phối đồ (Gemini Vision)**.

---

## 2. Tech Stack

| Thành phần | Công nghệ | Rationale |
|---|---|---|
| **Ngôn ngữ & Runtime** | Python 3.12+ | Hệ sinh thái AI/ML phong phú, tích hợp native với Google GenAI SDK |
| **Framework** | FastAPI | Hiệu năng cao, async-first, tự động sinh OpenAPI / Swagger UI, type-safe với Pydantic v2 |
| **Database** | MongoDB | Document database linh hoạt cho cấu trúc thuộc tính trang phục động, phân loại phong phú |
| **MongoDB Async Driver & ODM** | PyMongo (AsyncMongoClient) + Beanie ODM | Native async driver hiện đại, ODM tích hợp chặt chẽ với Pydantic v2 |
| **AI Text & Multimodal** | Google GenAI SDK (`google-genai`) — Model `gemini-flash-latest` | Tốc độ cao, chi phí tối ưu cho gợi ý phối đồ, giải thích văn hóa, phân tích ảnh |
| **AI Image Generation** | Google GenAI SDK — Model `imagen-4.0-generate-001` | Sinh hình ảnh minh họa chân thực cho các bộ trang phục |
| **File Storage** | Local Static Storage (`uploads/`) | Lưu trữ hình ảnh người dùng tải lên và ảnh tạo bởi AI (phục vụ qua StaticFiles) |
| **Validation & Serialization** | Pydantic v2 | Kiểm tra dữ liệu đầu vào, định dạng chuẩn response |
| **Testing** | Pytest + pytest-asyncio + HTTPX | Viết automated tests cho API async |
| **Environment Config** | pydantic-settings + python-dotenv | Quản lý cấu hình biến môi trường an toàn qua file `.env` |

---

## 3. Kiến trúc Tổng quan Hệ thống

```mermaid
flowchart TD
    subgraph Client["Frontend Client (Web / Mobile)"]
        FE["Giao diện người dùng"]
    end

    subgraph API["FastAPI Backend Service"]
        R["API Routers (v1)"]
        S["Service Layer (Business Logic)"]
        AI_T["Gemini Text Service\n(gemini-flash-latest)"]
        AI_I["Imagen Generation Service\n(imagen-4.0-generate-001)"]
        AI_V["Gemini Vision Analysis\n(gemini-flash-latest)"]
        V["Cultural Validation Engine\n(Quy tắc chuẩn hóa)"]
        FS["File Storage Handler\n(uploads/)"]
    end

    subgraph Data["Lớp Lưu trữ Dữ liệu"]
        DB[(MongoDB Database)]
        STATIC["Thư mục /uploads"]
        SEED["Dữ liệu gốc (CSV)"]
    end

    FE -->|"HTTP/JSON & Multipart"| R
    R --> S
    S --> AI_T
    S --> AI_I
    S --> AI_V
    S --> V
    S --> FS
    S --> DB
    FS --> STATIC
    SEED -->|"Seeding script"| DB
```

---

## 4. Thiết kế Database (MongoDB Collections)

Hệ thống sử dụng các Collection trong MongoDB:

### 4.1. `garment_types` (Loại trang phục gốc)
```json
{
  "_id": "ObjectId",
  "name": "Áo dài",
  "description": "Trang phục truyền thống của Việt Nam, nổi bật với áo vạt dài xẻ tà mặc cùng quần ống rộng..."
}
```

### 4.2. `categories` (Phân loại chi tiết)
Dữ liệu chuẩn hóa từ `listing.csv` và `description.csv`:
```json
{
  "_id": "ObjectId",
  "name": "Truyền thống",
  "description": "Phong cách thiết kế giữ nguyên các cấu trúc kinh điển...",
  "garment_type_id": "ObjectId",
  "occasions": ["Sự kiện", "Lễ nghi", "Dự tiệc", "Du lịch", "Công sở", "Thường nhật", "Học đường", "Tối giản"],
  "colors": ["Trắng", "Vàng nhạt", "Hồng", "Đỏ", "Xanh lam", "Xanh lá", "Pastel"],
  "fabrics": ["Vải lụa", "Vải gấm", "Vải voan", "Vải ren", "Vải nhung", "Vải cotton", "Vải phi"],
  "pattern_techniques": ["In", "Thêu", "Dệt", "Đính"],
  "patterns": ["Hoa (sen, đào, mai, cúc,...)", "Chim, phượng", "Mây, sóng, nước", "Trống đồng"],
  "accessories": ["Giày đế bằng, cao gót, guốc mộc", "Khăn quàng áo dài", "Túi gấm", "Mấn", "Trâm cài", "Kiềng cổ/Vòng ngọc", "Khuyên tai ngọc"],
  "structural_features": ["Cổ áo cao", "Thân áo ôm theo cơ thể (có thể bó sát hoặc không)", "Vạt dài", "Xẻ tà từ eo", "Tay dài", "Quần mềm, rộng, dài, phủ gần hoặc đến mắt cá chân, thường không có họa tiết"]
}
```

### 4.3. `components` (Bảng tra cứu thành phần)
Tập hợp toàn bộ thông tin chi tiết giải nghĩa từ `description.csv`:
```json
{
  "_id": "ObjectId",
  "type": "color",
  "name": "Đỏ",
  "description": "Tượng trưng cho sự may mắn, sung túc và hỷ sự, luôn là lựa chọn hàng đầu cho áo dài cưới hỏi, bưng quả hoặc dịp lễ Tết.",
  "hex_code": "#DC2626"
}
```
*Các loại `type`: `occasion` (Bối cảnh), `color` (Màu sắc), `fabric` (Chất liệu), `pattern_technique` (Phương pháp tạo họa tiết), `pattern` (Họa tiết), `accessory` (Phụ kiện), `structural_feature` (Đặc điểm cấu trúc).*

### 4.4. `not_recommended` (Quy tắc cảnh báo văn hóa)
Dữ liệu trích xuất từ `notrecommended.csv`:
```json
{
  "_id": "ObjectId",
  "components": ["Học đường", "Vải voan", "Vải ren", "Organza"],
  "reason": "Các chất liệu này thuộc hàng Truyền thống nhưng có độ mỏng và tính xuyên thấu cao, khi dùng trong môi trường giáo dục sẽ thiếu đi sự kín đáo, dễ gây hớ hênh và vi phạm quy chuẩn tác phong học đường."
}
```

### 4.5. `outfits` (Bộ phối đồ của người dùng)
```json
{
  "_id": "ObjectId",
  "name": "Áo dài lụa xanh lam thêu hoa sen",
  "category": "Truyền thống",
  "occasion": "Lễ nghi",
  "color": "Xanh lam",
  "fabric": "Vải lụa",
  "pattern_technique": "Thêu",
  "pattern": "Hoa (sen, đào, mai, cúc,...)",
  "accessories": ["Túi gấm", "Trâm cài", "Kiềng cổ/Vòng ngọc"],
  "structural_features": ["Cổ áo cao", "Vạt dài", "Xẻ tà từ eo"],
  "warnings": [],
  "cultural_info": "Áo dài lụa xanh lam thêu hoa sen mang ý nghĩa của sự tôn kính và thanh khiết...",
  "image_url": "/static/uploads/outfits/670abc.jpg",
  "created_at": "2026-10-08T14:40:00Z"
}
```

### 4.6. `lookbooks` (Bộ sưu tập & Chia sẻ)
```json
{
  "_id": "ObjectId",
  "title": "Lookbook Tết 2027",
  "description": "Bộ sưu tập áo dài chào xuân",
  "share_code": "vp-a1b2c3d4",
  "outfit_ids": ["ObjectId", "ObjectId"],
  "created_at": "2026-10-08T14:40:00Z"
}
```

### 4.7. `uploads` (Hình ảnh người dùng & Kết quả phân tích)
```json
{
  "_id": "ObjectId",
  "filename": "avatar_abc123.jpg",
  "original_filename": "my_photo.jpg",
  "file_path": "/static/uploads/users/avatar_abc123.jpg",
  "file_size": 204800,
  "mime_type": "image/jpeg",
  "upload_type": "avatar",
  "ai_analysis": {
    "detected_garment": "Áo dài truyền thống",
    "detected_colors": ["Trắng", "Xanh lam"],
    "body_type_suggestion": "Phom ôm vừa sẽ tôn vóc dáng...",
    "suggestions": ["Nên kết hợp cùng kiềng bạc để tạo điểm nhấn cổ điển"]
  },
  "created_at": "2026-10-08T14:40:00Z"
}
```

---

## 5. Danh sách API Endpoints Chi tiết

### 5.1. Nhóm Tra cứu Thành phần (Categories & Components)
- `GET /api/v1/categories`: Lấy danh sách 3 phân loại chính kèm các thuộc tính khả dụng.
- `GET /api/v1/categories/{id}`: Chi tiết phân loại theo ID hoặc tên (Truyền thống, Cách tân Nữ, Cách tân Nam).
- `GET /api/v1/components`: Lấy danh sách thành phần, hỗ trợ query filter `?type=color` và `?category=Truyền thống`.
- `GET /api/v1/components/{id}`: Tra cứu ý nghĩa và mô tả của 1 thành phần cụ thể.

### 5.2. Nhóm Phối đồ (Outfit Builder)
- `POST /api/v1/outfits`: Tạo bộ phối đồ mới. Hệ thống sẽ:
  1. Kiểm tra tính hợp lệ của các thành phần trong Category.
  2. Tự động chạy Cultural Validation Engine phát hiện xung đột văn hóa.
  3. Tự động sinh ý nghĩa văn hóa ngắn qua `gemini-flash-latest`.
  4. (Tùy chọn) Tự động sinh ảnh minh họa trang phục bằng `imagen-4.0`.
- `GET /api/v1/outfits`: Lấy danh sách bộ phối đồ đã lưu (phân trang).
- `GET /api/v1/outfits/{id}`: Xem chi tiết bộ trang phục.
- `DELETE /api/v1/outfits/{id}`: Xóa bộ trang phục.
- `POST /api/v1/outfits/{id}/generate-image`: Tạo hoặc sinh lại ảnh AI cho bộ trang phục.

### 5.3. Nhóm Kiểm tra Quy chuẩn Văn hóa (Validation)
- `POST /api/v1/validate`: Gửi thông tin phối đồ (Bối cảnh, Chất liệu, Màu sắc, Phụ kiện, Họa tiết) để kiểm tra cảnh báo tức thời.
  - Trả về `is_valid: true/false`, danh sách cảnh báo chi tiết lý do văn hóa và các gợi ý thay thế.

### 5.4. Nhóm Trợ lý AI Thông minh (Gemini AI Suggestions)
- `POST /api/v1/suggest`: Nhận câu hỏi ngôn ngữ tự nhiên của người dùng (ví dụ: *"Tôi muốn đi dự tiệc cưới bạn thân, phong cách thanh lịch nhưng không lấn át cô dâu"*), AI trích xuất thông số và gợi ý bộ phối phù hợp theo đúng dữ liệu chuẩn.
- `POST /api/v1/suggest/occasion`: Gợi ý trang phục nhanh dựa trên Sự kiện + Thời tiết (nóng/lạnh) + Giới tính.
- `POST /api/v1/color-harmony`: Phân tích mức độ hài hòa màu sắc giữa áo, quần, và phụ kiện trong truyền thống Việt Nam.
- `POST /api/v1/compare`: So sánh 2 đến 4 bộ trang phục theo tiêu chí: Mức độ trang trọng (Formality), Tính bảo tồn văn hóa (Authenticity), Tính linh hoạt (Versatility).

### 5.5. Nhóm Sinh Hình ảnh & Thử đồ AI (Image Generation & Try-on)
- `POST /api/v1/images/generate`: Tạo ảnh phối đồ độc lập theo mô tả chi tiết, bối cảnh nền (Hoàng Thành Huế, Phố cổ Hội An, Hồ Gươm, Studio...).
- `POST /api/v1/images/try-on`: Mô phỏng phối đồ dựa trên avatar/ảnh người dùng tải lên kết hợp trang phục đã chọn.

### 5.6. Nhóm Tải lên Tệp (Uploads & Vision Analysis)
- `POST /api/v1/uploads`: Tải lên ảnh chân dung/avatar/ảnh mẫu (Multipart form-data). Tự động nén/resize và dùng Gemini Vision để phân tích đặc điểm, màu sắc, gợi ý phom dáng.
- `GET /api/v1/uploads/{id}`: Lấy thông tin tệp tải lên và kết quả phân tích.
- `DELETE /api/v1/uploads/{id}`: Xóa tệp tải lên.

### 5.7. Nhóm Lookbook & Chia sẻ (Lookbook Sharing)
- `POST /api/v1/lookbooks`: Tạo Lookbook mới từ danh sách các outfit.
- `GET /api/v1/lookbooks`: Danh sách Lookbook.
- `GET /api/v1/lookbooks/{id}`: Chi tiết Lookbook.
- `GET /api/v1/lookbooks/shared/{share_code}`: Truy cập công khai Lookbook qua mã chia sẻ (ví dụ: `vp-a8f3b21c`).
- `PUT /api/v1/lookbooks/{id}`: Chỉnh sửa thông tin Lookbook.
- `DELETE /api/v1/lookbooks/{id}`: Xóa Lookbook.
- `POST /api/v1/lookbooks/{id}/outfits`: Thêm outfit vào Lookbook.
- `DELETE /api/v1/lookbooks/{id}/outfits/{outfit_id}`: Gỡ outfit khỏi Lookbook.

---

## 6. Cấu trúc Thư mục Dự án

```
D:\Projects\du-an-ma\
├── .env                       # Biến môi trường (API Key, MongoDB config)
├── requirements.txt           # Thư viện phụ thuộc Python
├── data/                      # Dữ liệu nguồn từ chuyên gia
│   ├── description.csv        # Mô tả ý nghĩa 70 thành phần
│   ├── listing.csv            # Bảng phối chuẩn cho 3 đối tượng
│   └── notrecommended.csv     # 16 quy tắc cấm kỵ/cảnh báo văn hóa
├── docs/                      # Tài liệu dự án
│   ├── REQUIREMENTS.md        # Yêu cầu bài toán
│   └── PLAN.md                # Kế hoạch thiết kế backend API này
├── uploads/                   # Lưu trữ tệp tĩnh
│   ├── outfits/               # Ảnh sinh cho các bộ phối đồ
│   ├── generated/             # Ảnh sinh theo yêu cầu tự do
│   ├── tryon/                 # Ảnh kết quả thử trang phục
│   └── users/                 # Ảnh tải lên của người dùng
├── app/                       # Mã nguồn Backend FastAPI
│   ├── __init__.py
│   ├── main.py                # Điểm khởi chạy FastAPI ứng dụng
│   ├── config.py              # Cấu hình Pydantic Settings đọc .env
│   ├── database.py            # Khởi tạo kết nối PyMongo & Beanie ODM
│   ├── seed.py                # Script nạp dữ liệu từ CSV vào MongoDB
│   ├── models/                # Document Models (Beanie)
│   │   ├── __init__.py
│   │   ├── garment.py         # GarmentType & Category
│   │   ├── component.py       # Component (bối cảnh, màu, chất liệu...)
│   │   ├── outfit.py          # Outfit
│   │   ├── lookbook.py        # Lookbook
│   │   ├── upload.py          # Upload
│   │   └── not_recommended.py # NotRecommended rule
│   ├── schemas/               # Request/Response Pydantic Schemas
│   │   ├── __init__.py
│   │   ├── component.py
│   │   ├── outfit.py
│   │   ├── lookbook.py
│   │   ├── validation.py
│   │   ├── suggestion.py
│   │   ├── image.py
│   │   └── upload.py
│   ├── routers/               # Định tuyến API Endpoints
│   │   ├── __init__.py
│   │   ├── categories.py
│   │   ├── components.py
│   │   ├── outfits.py
│   │   ├── validation.py
│   │   ├── suggestions.py
│   │   ├── images.py
│   │   ├── uploads.py
│   │   ├── lookbooks.py
│   │   └── compare.py
│   ├── services/              # Xử lý Logic Nghiệp vụ
│   │   ├── __init__.py
│   │   ├── component_service.py
│   │   ├── outfit_service.py
│   │   ├── validation_service.py
│   │   ├── suggestion_service.py
│   │   ├── image_service.py
│   │   ├── upload_service.py
│   │   ├── lookbook_service.py
│   │   └── compare_service.py
│   └── ai/                    # Tích hợp AI (Google GenAI SDK)
│       ├── __init__.py
│       ├── client.py          # AI Client wrapper (Gemini + Imagen)
│       ├── prompts.py         # System prompt & template tiếng Việt
│       └── image_gen.py       # Pipeline sinh ảnh trang phục
└── tests/                     # Automated Test Suite
    ├── __init__.py
    ├── conftest.py            # Test fixtures & mock DB/AI
    ├── test_components.py
    ├── test_outfits.py
    ├── test_validation.py
    ├── test_suggestions.py
    └── test_uploads.py
```

---

## 7. Cấu hình Môi trường (`.env`)

Tách biệt rõ ràng từng trường thông tin của MongoDB để người dùng có thể dễ dàng điền dù chạy Local hay Cloud (MongoDB Atlas):

```bash
# Gemini AI API Key
GEMINI_API_KEY=...

# MongoDB — Điền thông tin kết nối của bạn
MONGODB_HOST=
MONGODB_PORT=27017
MONGODB_USERNAME=
MONGODB_PASSWORD=
MONGODB_NAME=vietphuc_remix
```

*Trong code `app/config.py`: Sẽ có thuộc tính tự động tổng hợp kết nối:*
- *Nếu có `MONGODB_USERNAME` & `MONGODB_PASSWORD` -> Kết nối theo dạng SRV MongoDB Atlas: `mongodb+srv://user:pass@host/name`*
- *Nếu không có xác thực -> Kết nối Local: `mongodb://host:port/name`*

---

## 8. Kế hoạch Kiểm thử & Đảm bảo Chất lượng

### Automated Tests
1. **Kiểm tra nạp dữ liệu (Seeding Test)**: Xác nhận 3 phân loại, 70 thành phần, và 16 quy tắc cấm kỵ được nạp chính xác từ CSV.
2. **Kiểm tra Logic Quy tắc Văn hóa (Validation Test)**:
   - Thử nghiệm kết hợp "Học đường + Vải voan" -> Cảnh báo vi phạm độ kín đáo.
   - Thử nghiệm kết hợp "Công sở + Mấn + Kiềng cổ" -> Cảnh báo quá rườm rà.
   - Thử nghiệm kết hợp hợp lệ -> `is_valid: true`.
3. **Kiểm tra CRUD Outfit & Lookbook**: Tạo, đọc, cập nhật mã chia sẻ, xóa.
4. **Kiểm tra Upload Tệp**: Kiểm tra định dạng cho phép, giới hạn dung lượng 10MB, lưu trữ tệp an toàn.
5. **Kiểm tra Graceful Degradation của AI**: Nếu API key hết quota hoặc không có kết nối mạng, hệ thống tự động fallback về văn bản mặc định mà không làm sập API.
