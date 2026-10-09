import os
import csv
import asyncio
import logging
from app.database import connect_db, close_db, is_connected
from app.models import GarmentType, Category, Component, NotRecommended
from app.services.component_service import COLOR_HEX_MAP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vietphuc.seed")

async def seed_data():
    """Nạp toàn bộ dữ liệu từ 3 file CSV vào MongoDB."""
    logger.info("Bắt đầu kết nối database để nạp dữ liệu...")
    await connect_db()
    
    if not is_connected:
        logger.error("❌ Không thể kết nối tới MongoDB! Vui lòng đảm bảo MongoDB đang chạy và cấu hình .env chính xác.")
        return

    logger.info("Dọn dẹp dữ liệu cũ...")
    await GarmentType.find_all().delete()
    await Category.find_all().delete()
    await Component.find_all().delete()
    await NotRecommended.find_all().delete()

    # 1. Tạo GarmentType (Áo dài)
    ao_dai = GarmentType(
        name="Áo dài",
        description="Trang phục truyền thống của Việt Nam, nổi bật với áo vạt dài xẻ tà mặc cùng quần ống rộng, tôn vinh vẻ đẹp kín đáo và thanh lịch."
    )
    await ao_dai.insert()
    logger.info(f"✅ Đã tạo GarmentType: {ao_dai.name}")

    # 2. Đọc description.csv để chuẩn bị mô tả
    descriptions_map = {}
    desc_path = os.path.join("data", "description.csv")
    if os.path.exists(desc_path):
        with open(desc_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                comp = row.get("component", "").strip()
                desc = row.get("description", "").strip()
                if comp:
                    descriptions_map[comp] = desc

    # 3. Đọc listing.csv và nạp Categories
    listing_path = os.path.join("data", "listing.csv")
    cat_count = 0
    if os.path.exists(listing_path):
        with open(listing_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("Phân loại / Đối tượng", "").strip()
                if not name:
                    continue
                
                cat = Category(
                    name=name,
                    description=descriptions_map.get(name, f"Phong cách {name}"),
                    garment_type_id=str(ao_dai.id),
                    occasions=[x.strip() for x in row.get("Bối cảnh", "").split("/") if x.strip()],
                    colors=[x.strip() for x in row.get("Màu sắc", "").split("/") if x.strip()],
                    fabrics=[x.strip() for x in row.get("Chất liệu", "").split("/") if x.strip()],
                    pattern_techniques=[x.strip() for x in row.get("Phương pháp tạo họa tiết", "").split("/") if x.strip()],
                    patterns=[x.strip() for x in row.get("Họa tiết", "").split("/") if x.strip()],
                    accessories=[x.strip() for x in row.get("Phụ kiện", "").split("/") if x.strip()],
                    structural_features=[],
                )
                await cat.insert()
                cat_count += 1
    logger.info(f"✅ Đã nạp {cat_count} Categories từ listing.csv")

    # 4. Nạp Components từ description.csv
    comp_count = 0
    if os.path.exists(desc_path):
        with open(desc_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                comp_name = row.get("component", "").strip()
                comp_desc = row.get("description", "").strip()
                if not comp_name or comp_name in ["Áo dài", "Truyền thống", "Cách tân - Nữ", "Cách tân - Nam"]:
                    continue

                ctype = "structural_feature"
                name_l = comp_name.lower()
                if any(c in name_l for c in ["trắng", "vàng", "hồng", "đỏ", "xanh", "pastel"]):
                    ctype = "color"
                elif any(f in name_l for f in ["vải", "lụa", "gấm", "voan", "ren", "nhung", "cotton", "phi", "tafta", "linen", "organza"]):
                    ctype = "fabric"
                elif any(p in name_l for p in ["in", "thêu", "dệt", "đính", "xếp ly", "vẽ tay"]):
                    ctype = "pattern_technique"
                elif any(pt in name_l for pt in ["hoa", "chim", "mây", "trống đồng", "trừu tượng", "linh vật", "điểm hoa", "hình học"]):
                    ctype = "pattern"
                elif any(a in name_l for a in ["giày", "guốc", "khăn", "túi", "mấn", "trâm", "kiềng", "khuyên", "vòng", "bờm", "ghim", "tua"]):
                    ctype = "accessory"
                elif any(o in name_l for o in ["sự kiện", "lễ nghi", "dự tiệc", "du lịch", "công sở", "thường nhật", "học đường", "tối giản", "dạo phố"]):
                    ctype = "occasion"

                comp = Component(
                    type=ctype,
                    name=comp_name,
                    description=comp_desc,
                    hex_code=COLOR_HEX_MAP.get(name_l),
                )
                await comp.insert()
                comp_count += 1
    logger.info(f"✅ Đã nạp {comp_count} Components từ description.csv")

    # 5. Nạp NotRecommended từ notrecommended.csv
    nr_count = 0
    nr_path = os.path.join("data", "notrecommended.csv")
    if os.path.exists(nr_path):
        with open(nr_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            for row in reader:
                dresscode = row.get("dresscode", "").strip()
                reason = row.get("reason", "").strip()
                if dresscode:
                    items = [x.strip() for x in dresscode.split("/") if x.strip()]
                    nr = NotRecommended(
                        components=items,
                        reason=reason,
                    )
                    await nr.insert()
                    nr_count += 1
    logger.info(f"✅ Đã nạp {nr_count} NotRecommended rules từ notrecommended.csv")

    await close_db()
    logger.info("🎉 Hoàn tất quá trình Seed dữ liệu vào MongoDB!")

if __name__ == "__main__":
    asyncio.run(seed_data())
