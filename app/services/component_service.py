import os
import csv
from typing import List, Optional, Dict, Any
from app.models.garment import Category, GarmentType
from app.models.component import Component
from app.database import is_connected

COLOR_HEX_MAP = {
    "trắng": "#FFFFFF",
    "vàng nhạt": "#FEF08A",
    "hồng": "#F472B6",
    "đỏ": "#DC2626",
    "xanh lam": "#2563EB",
    "xanh lá": "#16A34A",
    "pastel": "#E2E8F0",
}

# In-memory CSV cache for offline fallback
CSV_CATEGORIES_CACHE: List[Dict[str, Any]] = []
CSV_COMPONENTS_CACHE: List[Dict[str, Any]] = []

def load_csv_data():
    global CSV_CATEGORIES_CACHE, CSV_COMPONENTS_CACHE
    
    # 1. Parse listing.csv for categories
    listing_path = os.path.join("data", "listing.csv")
    if os.path.exists(listing_path) and not CSV_CATEGORIES_CACHE:
        with open(listing_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                name = row.get("Phân loại / Đối tượng", "").strip()
                if not name:
                    continue
                CSV_CATEGORIES_CACHE.append({
                    "id": f"cat_{idx+1}",
                    "name": name,
                    "description": "",
                    "occasions": [x.strip() for x in row.get("Bối cảnh", "").split("/") if x.strip()],
                    "colors": [x.strip() for x in row.get("Màu sắc", "").split("/") if x.strip()],
                    "fabrics": [x.strip() for x in row.get("Chất liệu", "").split("/") if x.strip()],
                    "pattern_techniques": [x.strip() for x in row.get("Phương pháp tạo họa tiết", "").split("/") if x.strip()],
                    "patterns": [x.strip() for x in row.get("Họa tiết", "").split("/") if x.strip()],
                    "accessories": [x.strip() for x in row.get("Phụ kiện", "").split("/") if x.strip()],
                    "structural_features": [],
                })

    # 2. Parse description.csv for components & category descriptions
    desc_path = os.path.join("data", "description.csv")
    if os.path.exists(desc_path) and not CSV_COMPONENTS_CACHE:
        with open(desc_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                comp_name = row.get("component", "").strip()
                comp_desc = row.get("description", "").strip()
                if not comp_name:
                    continue

                # Cập nhật mô tả cho category nếu khớp
                for cat in CSV_CATEGORIES_CACHE:
                    if cat["name"].lower() == comp_name.lower():
                        cat["description"] = comp_desc

                # Xác định component type
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

                hex_val = COLOR_HEX_MAP.get(name_l)
                CSV_COMPONENTS_CACHE.append({
                    "id": f"comp_{idx+1}",
                    "type": ctype,
                    "name": comp_name,
                    "description": comp_desc,
                    "hex_code": hex_val,
                    "image_url": None,
                })

load_csv_data()

async def get_all_categories() -> List[Dict[str, Any]]:
    """Lấy danh sách các phân loại trang phục."""
    if is_connected:
        try:
            cats = await Category.find_all().to_list()
            if cats:
                return [
                    {
                        "id": str(c.id),
                        "name": c.name,
                        "description": c.description,
                        "occasions": c.occasions,
                        "colors": c.colors,
                        "fabrics": c.fabrics,
                        "pattern_techniques": c.pattern_techniques,
                        "patterns": c.patterns,
                        "accessories": c.accessories,
                        "structural_features": c.structural_features,
                    }
                    for c in cats
                ]
        except Exception:
            pass
    return CSV_CATEGORIES_CACHE

async def get_category_by_id(cat_id: str) -> Optional[Dict[str, Any]]:
    """Lấy chi tiết 1 category."""
    cats = await get_all_categories()
    for c in cats:
        if c["id"] == cat_id or c["name"].lower() == cat_id.lower():
            return c
    return None

async def get_components(
    type_filter: Optional[str] = None,
    category_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Lấy danh sách components có filter."""
    if is_connected:
        try:
            query = {}
            if type_filter:
                query["type"] = type_filter
            db_comps = await Component.find(query).to_list()
            if db_comps:
                items = [
                    {
                        "id": str(c.id),
                        "type": c.type,
                        "name": c.name,
                        "description": c.description,
                        "hex_code": c.hex_code or COLOR_HEX_MAP.get(c.name.lower()),
                        "image_url": c.image_url,
                    }
                    for c in db_comps
                ]
                if category_filter:
                    cat = await get_category_by_id(category_filter)
                    if cat:
                        allowed_names = set(
                            cat["occasions"] + cat["colors"] + cat["fabrics"] +
                            cat["pattern_techniques"] + cat["patterns"] + cat["accessories"]
                        )
                        items = [i for i in items if i["name"] in allowed_names]
                return items
        except Exception:
            pass

    # Fallback to CSV
    items = list(CSV_COMPONENTS_CACHE)
    if type_filter:
        items = [i for i in items if i["type"] == type_filter]
    if category_filter:
        cat = await get_category_by_id(category_filter)
        if cat:
            allowed_names = set(
                cat["occasions"] + cat["colors"] + cat["fabrics"] +
                cat["pattern_techniques"] + cat["patterns"] + cat["accessories"]
            )
            items = [i for i in items if i["name"] in allowed_names]
    return items

async def get_component_by_id(comp_id: str) -> Optional[Dict[str, Any]]:
    """Lấy chi tiết 1 component."""
    comps = await get_components()
    for c in comps:
        if c["id"] == comp_id or c["name"].lower() == comp_id.lower():
            return c
    return None
