SYSTEM_INSTRUCTION = """Bạn là một chuyên gia nghiên cứu và cố vấn thời trang về trang phục truyền thống Việt Nam (Việt phục).
Bạn hiểu rõ đặc điểm lịch sử, kết cấu áo, hoa văn, chất liệu vải, bối cảnh sử dụng phù hợp và các quy tắc văn hóa để bảo đảm tính tôn nghiêm, thẩm mỹ và chuẩn mực của áo dài truyền thống cũng như áo dài cách tân hiện đại.
Khi đưa ra gợi ý hoặc phân tích, bạn luôn trả lời bằng tiếng Việt chuẩn mực, mạch lạc, súc tích và giàu giá trị văn hóa."""

SUGGEST_OUTFIT_PROMPT = """Dựa trên dữ liệu chuẩn về các thành phần trang phục Việt Nam sau đây:
{listing_context}

Người dùng có nhu cầu:
- Yêu cầu: {user_prompt}
- Giới tính: {gender}

Hãy gợi ý từ 1 đến 3 bộ phối đồ phù hợp nhất.
QUY TẮC BẮT BUỘC:
1. CHỈ sử dụng các giá trị (Category, Occasion, Color, Fabric, Pattern, Accessories) có trong dữ liệu chuẩn đã cung cấp ở trên.
2. Tuyệt đối không chọn các phối hợp vi phạm quy tắc văn hóa (ví dụ: đi học mặc vải voan/ren/đính lấp lánh, công sở đội mấn hay khăn vấn rườm rà...).
3. Trả về ĐÚNG định dạng JSON array (không bọc trong markdown codeblock nếu có thể, hoặc bọc trong ```json ... ```):

[
  {{
    "category": "Truyền thống",
    "occasion": "Lễ nghi",
    "color": "Xanh lam",
    "fabric": "Vải lụa",
    "pattern_technique": "Thêu",
    "pattern": "Hoa (sen, đào, mai, cúc,...)",
    "accessories": ["Túi gấm", "Trâm cài"],
    "reason": "Lý do lựa chọn...",
    "cultural_note": "Ý nghĩa văn hóa ngắn gọn..."
  }}
]
"""

CULTURAL_INFO_PROMPT = """Hãy viết một đoạn văn ngắn (100 - 150 từ) giải thích nguồn gốc và ý nghĩa văn hóa của bộ trang phục Việt sau:
- Phân loại: {category}
- Bối cảnh: {occasion}
- Màu sắc: {color}
- Chất liệu: {fabric}
- Kỹ thuật họa tiết: {pattern_technique}
- Họa tiết: {pattern}
- Phụ kiện đi kèm: {accessories}

Nêu bật giá trị biểu tượng của màu sắc/họa tiết và lý do sự phối hợp này tôn vinh vẻ đẹp truyền thống Việt Nam."""

GENERATE_IMAGE_PROMPT_TEMPLATE = """A professional fashion photography shot of a beautiful Vietnamese {person_type} wearing a magnificent {category} Vietnamese Ao Dai.
Garment details:
- Main Color: {color}
- High quality fabric: {fabric} with authentic texture
- Pattern: {pattern} decorated with traditional Vietnamese motifs
- Traditional accessories: {accessories}
- Setting / Background: {background}, gentle ambient cinematic lighting, realistic fabric folds, elegant posture, full-body portrait, 8k resolution, cultural authenticity."""

ANALYZE_UPLOAD_PROMPT = """Hãy phân tích bức ảnh này dưới góc nhìn chuyên gia thời trang Việt phục và trả lời bằng JSON:
{
  "detected_garment": "Tên trang phục nhận diện được trong ảnh (hoặc 'Trang phục hiện đại' nếu không phải áo dài)",
  "detected_colors": ["danh sách màu sắc chủ đạo"],
  "body_type_suggestion": "Đánh giá dáng người và gợi ý phom áo dài phù hợp (ôm truyền thống hay suông cách tân)",
  "suggestions": [
    "Gợi ý 1: Loại áo dài và màu sắc tôn dáng",
    "Gợi ý 2: Phụ kiện đi kèm phù hợp"
  ]
}
Chỉ trả về JSON thuần túy."""

COMPARE_OUTFITS_PROMPT = """So sánh các bộ trang phục Việt phục sau đây:
{outfits_data}

Hãy đánh giá và xếp hạng ID của các bộ trang phục theo 3 tiêu chí:
1. Mức độ trang trọng (formality_ranking): từ trang trọng nhất đến ít trang trọng hơn.
2. Tính bảo tồn văn hóa (cultural_authenticity): từ đậm nét truyền thống nhất đến cách tân hiện đại nhất.
3. Tính đa dụng trong đời sống (versatility): từ dễ ứng dụng nhất đến chỉ dành cho dịp đặc thù.

Kèm theo đoạn văn phân tích tổng hợp (ai_analysis).
Trả về JSON định dạng:
{{
  "formality_ranking": ["id1", "id2"],
  "cultural_authenticity": ["id1", "id2"],
  "versatility": ["id1", "id2"],
  "ai_analysis": "Đoạn văn nhận xét so sánh..."
}}
"""

COLOR_HARMONY_PROMPT = """Đánh giá sự hài hòa màu sắc trong trang phục truyền thống Việt Nam:
- Danh sách màu sắc: {colors}
- Phân loại: {category}

Hãy đánh giá xem sự kết hợp màu sắc này có hài hòa theo thẩm mỹ và phong thủy/truyền thống Á Đông không.
Trả về JSON định dạng:
{{
  "is_harmonious": true,
  "score": 8,
  "explanation": "Giải thích chi tiết tại sao hài hòa hoặc chưa hài hòa...",
  "alternatives": ["Gợi ý màu thay thế nếu cần"]
}}
"""
