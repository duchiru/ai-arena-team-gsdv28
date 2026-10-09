import os
import csv
from typing import List, Optional, Dict, Any
from app.models.not_recommended import NotRecommended
from app.database import is_connected

KNOWN_CONTEXTS = {
    "học đường", "công sở", "tối giản", "thường nhật",
    "dạo phố", "sự kiện", "dự tiệc", "lễ nghi", "du lịch"
}

# Fallback in-memory cache loaded from CSV if DB is not available
CSV_RULES_CACHE: List[Dict[str, Any]] = []

def load_csv_rules():
    global CSV_RULES_CACHE
    csv_path = os.path.join("data", "notrecommended.csv")
    if os.path.exists(csv_path) and not CSV_RULES_CACHE:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            for row in reader:
                dresscode = row.get("dresscode", "").strip()
                reason = row.get("reason", "").strip()
                if dresscode:
                    items = [x.strip() for x in dresscode.split("/") if x.strip()]
                    CSV_RULES_CACHE.append({"components": items, "reason": reason})

load_csv_rules()

async def validate_combination(
    category: Optional[str] = None,
    occasion: Optional[str] = None,
    color: Optional[str] = None,
    fabric: Optional[str] = None,
    pattern_technique: Optional[str] = None,
    pattern: Optional[str] = None,
    accessories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Kiểm tra xung đột quy tắc văn hóa."""
    # 1. Thu thập bối cảnh và các thuộc tính người dùng chọn
    user_occasion_str = (occasion or "").strip().lower()
    user_category_str = (category or "").strip().lower()

    # Thu thập tất cả các item người dùng chọn ngoài bối cảnh
    user_items: List[str] = []
    for val in [color, fabric, pattern_technique, pattern]:
        if val:
            user_items.append(val.strip().lower())
    if accessories:
        for acc in accessories:
            if acc:
                user_items.append(acc.strip().lower())

    # 2. Lấy danh sách rules từ MongoDB hoặc CSV fallback
    rules = []
    if is_connected:
        try:
            db_rules = await NotRecommended.find_all().to_list()
            rules = [{"components": r.components, "reason": r.reason} for r in db_rules]
        except Exception:
            rules = CSV_RULES_CACHE
    else:
        rules = CSV_RULES_CACHE

    warnings = []

    # 3. Đối chiếu kiểm tra xung đột
    for rule in rules:
        rule_components = rule.get("components", [])
        reason = rule.get("reason", "")
        if not rule_components:
            continue

        # Phân loại thành phần trong rule thành: Bối cảnh (contexts) và Thành phần xung đột (items)
        rule_contexts = [c for c in rule_components if c.lower() in KNOWN_CONTEXTS]
        rule_items = [c for c in rule_components if c.lower() not in KNOWN_CONTEXTS]

        # Nếu rule không chứa context nào, coi thành phần đầu tiên là context
        if not rule_contexts and len(rule_components) > 1:
            rule_contexts = [rule_components[0]]
            rule_items = rule_components[1:]

        # Kiểm tra xem bối cảnh của user có khớp với bối cảnh của rule không
        context_matched = False
        matched_context_name = ""
        for rc in rule_contexts:
            rc_lower = rc.lower()
            if (user_occasion_str and (rc_lower in user_occasion_str or user_occasion_str in rc_lower)) or \
               (user_category_str and (rc_lower in user_category_str or user_category_str in rc_lower)):
                context_matched = True
                matched_context_name = rc
                break

        # Nếu có chỉ định bối cảnh nhưng không khớp với rule này -> Bỏ qua
        if user_occasion_str and not context_matched:
            continue

        # Nếu khớp bối cảnh (hoặc user không truyền bối cảnh):
        # Kiểm tra xem có thành phần xung đột nào xuất hiện trong lựa chọn của user không
        matched_rule_items = []
        for ri in rule_items:
            ri_lower = ri.lower()
            for u_item in user_items:
                if ri_lower in u_item or u_item in ri_lower:
                    matched_rule_items.append(ri)
                    break

        if matched_rule_items:
            # Nếu user có bối cảnh khớp VÀ có thành phần xung đột
            # Hoặc không có bối cảnh nhưng xuất hiện từ 2 thành phần xung đột trở lên
            if context_matched or len(matched_rule_items) >= 2:
                involved_components = [matched_context_name] + matched_rule_items if matched_context_name else matched_rule_items
                warnings.append({
                    "severity": "warning",
                    "components": involved_components,
                    "reason": reason,
                })

    # 4. Gợi ý thay thế nếu có vi phạm
    suggestions = []
    if warnings:
        suggestions.append("Tham khảo các chất liệu truyền thống như Lụa tơ tằm, Gấm hoa nền nã.")
        suggestions.append("Tiết chế phụ kiện để giữ trọn vẻ đẹp thanh lịch chuẩn mực.")

    return {
        "is_valid": len(warnings) == 0,
        "warnings": warnings,
        "suggestions": suggestions,
    }
