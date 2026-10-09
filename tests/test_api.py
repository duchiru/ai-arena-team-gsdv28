import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.mark.asyncio
async def test_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "Việt Phục Remix API"
    assert data["version"] == "2.0.0"

@pytest.mark.asyncio
async def test_get_categories():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/categories/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["total"] >= 3
    names = [c["name"] for c in data["items"]]
    assert "Truyền thống" in names

@pytest.mark.asyncio
async def test_get_components():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Lọc màu sắc
        response = await ac.get("/api/v1/components/?type=color")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    for item in data["items"]:
        assert item["type"] == "color"
        assert item["hex_code"] is not None

@pytest.mark.asyncio
async def test_validation_valid():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "category": "Truyền thống",
            "occasion": "Lễ nghi",
            "color": "Đỏ",
            "fabric": "Vải lụa",
            "accessories": ["Kiềng cổ/Vòng ngọc"]
        }
        response = await ac.post("/api/v1/validate/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is True
    assert len(data["warnings"]) == 0

@pytest.mark.asyncio
async def test_validation_invalid_school_voan():
    """Học đường + Vải voan -> Phải phát hiện cảnh báo văn hóa."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "category": "Truyền thống",
            "occasion": "Học đường",
            "color": "Trắng",
            "fabric": "Vải voan",
            "accessories": []
        }
        response = await ac.post("/api/v1/validate/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is False
    assert len(data["warnings"]) > 0
    assert any("mỏng" in w["reason"].lower() or "kín đáo" in w["reason"].lower() for w in data["warnings"])

@pytest.mark.asyncio
async def test_validation_invalid_office_man():
    """Công sở + Mấn + Kiềng cổ -> Quá cồng kềnh chốn văn phòng."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "category": "Truyền thống",
            "occasion": "Công sở",
            "color": "Xanh lam",
            "fabric": "Vải lụa",
            "accessories": ["Mấn", "Kiềng cổ/Vòng ngọc"]
        }
        response = await ac.post("/api/v1/validate/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is False
    assert len(data["warnings"]) > 0

@pytest.mark.asyncio
async def test_outfit_crud():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Tạo outfit
        create_payload = {
            "category": "Truyền thống",
            "occasion": "Lễ nghi",
            "color": "Xanh lam",
            "fabric": "Vải lụa",
            "pattern_technique": "Thêu",
            "pattern": "Hoa (sen, đào, mai, cúc,...)",
            "accessories": ["Túi gấm", "Trâm cài"],
            "custom_name": "Áo dài lam ngọc trâm cài",
            "generate_image": False
        }
        res_create = await ac.post("/api/v1/outfits/", json=create_payload)
        assert res_create.status_code == 201
        created = res_create.json()
        assert created["name"] == "Áo dài lam ngọc trâm cài"
        outfit_id = created["id"]

        # 2. Lấy chi tiết
        res_get = await ac.get(f"/api/v1/outfits/{outfit_id}")
        assert res_get.status_code == 200
        assert res_get.json()["id"] == outfit_id

        # 3. Lấy danh sách
        res_list = await ac.get("/api/v1/outfits/")
        assert res_list.status_code == 200
        assert res_list.json()["total"] >= 1

        # 4. Xóa
        res_del = await ac.delete(f"/api/v1/outfits/{outfit_id}")
        assert res_del.status_code == 200

@pytest.mark.asyncio
async def test_ai_suggestions():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "prompt": "Tôi muốn mặc áo dài đi dự đám cưới người quen",
            "gender": "female"
        }
        response = await ac.post("/api/v1/suggest/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert len(data["suggestions"]) > 0

@pytest.mark.asyncio
async def test_color_harmony():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "colors": ["Hồng", "Trắng"],
            "category": "Truyền thống"
        }
        response = await ac.post("/api/v1/suggest/color-harmony", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "is_harmonious" in data
    assert "score" in data

@pytest.mark.asyncio
async def test_lookbook_sharing():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Tạo lookbook
        payload = {
            "title": "Lookbook Tết Hà Nội",
            "description": "Những mẫu áo dài du xuân phố cổ",
            "outfit_ids": []
        }
        res = await ac.post("/api/v1/lookbooks/", json=payload)
        assert res.status_code == 201
        lb = res.json()
        assert lb["share_code"].startswith("vp-")
        share_code = lb["share_code"]

        # Xem qua mã chia sẻ
        res_shared = await ac.get(f"/api/v1/lookbooks/shared/{share_code}")
        assert res_shared.status_code == 200
        assert res_shared.json()["title"] == "Lookbook Tết Hà Nội"

@pytest.mark.asyncio
async def test_upload_file():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {
            "file": ("test_avatar.jpg", b"\xFF\xD8\xFF\xE0\x00\x10JFIF" + b"\x00" * 100, "image/jpeg")
        }
        data = {"upload_type": "avatar"}
        response = await ac.post("/api/v1/uploads/", files=files, data=data)
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["upload_type"] == "avatar"
    assert "file_url" in res_json
