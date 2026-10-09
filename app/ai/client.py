import logging
import json
import re
from typing import Optional, Dict, Any, List
from google import genai
from google.genai import types
from app.config import settings
from app.ai.prompts import SYSTEM_INSTRUCTION

logger = logging.getLogger("vietphuc.ai")

class AIClient:
    def __init__(self):
        self._client: Optional[genai.Client] = None

    @property
    def client(self) -> Optional[genai.Client]:
        if self._client is None and settings.GEMINI_API_KEY:
            try:
                self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
            except Exception as e:
                logger.error(f"Lỗi khởi tạo Gemini Client: {e}")
        return self._client

    async def generate_text(self, prompt: str, system_instruction: str = SYSTEM_INSTRUCTION) -> str:
        """Sinh văn bản bằng Gemini Flash."""
        if not self.client:
            logger.warning("Gemini Client chưa được cấu hình API Key.")
            return "Dịch vụ AI chưa sẵn sàng (vui lòng cấu hình GEMINI_API_KEY)."

        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=config,
            )
            return response.text or ""
        except Exception as e:
            logger.error(f"Lỗi gọi Gemini generate_text: {e}")
            return f"Không thể lấy phản hồi từ AI: {str(e)}"

    async def generate_json(self, prompt: str, system_instruction: str = SYSTEM_INSTRUCTION) -> Any:
        """Sinh nội dung và parse kết quả JSON an toàn."""
        raw_text = await self.generate_text(prompt, system_instruction)
        
        # Làm sạch chuỗi markdown ```json ... ```
        cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text.strip(), flags=re.MULTILINE)
        cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE).strip()
        
        try:
            return json.loads(cleaned)
        except Exception as e:
            logger.warning(f"Không thể parse JSON từ AI text: {raw_text}. Error: {e}")
            return None

    async def analyze_image(self, image_bytes: bytes, mime_type: str, prompt: str) -> Optional[Dict[str, Any]]:
        """Phân tích hình ảnh bằng Gemini Multimodal/Vision."""
        if not self.client:
            logger.warning("Gemini Client chưa được cấu hình API Key.")
            return None

        try:
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    prompt,
                ],
            )
            raw_text = response.text or "{}"
            cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text.strip(), flags=re.MULTILINE)
            cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE).strip()
            return json.loads(cleaned)
        except Exception as e:
            logger.error(f"Lỗi phân tích ảnh bằng Gemini Vision: {e}")
            return {"error": f"Lỗi phân tích hình ảnh: {str(e)}"}

    async def generate_image(self, prompt: str) -> Optional[bytes]:
        """Tạo hình ảnh bằng Imagen 4.0."""
        if not self.client:
            logger.warning("Gemini Client chưa được cấu hình API Key để sinh ảnh.")
            return None

        try:
            response = self.client.models.generate_images(
                model=settings.IMAGEN_MODEL,
                prompt=prompt,
                config=types.GenerateImageConfig(
                    number_of_images=1,
                    output_mime_type="image/jpeg",
                ),
            )
            if response.generated_images and len(response.generated_images) > 0:
                return response.generated_images[0].image.image_bytes
            return None
        except Exception as e:
            logger.error(f"Lỗi tạo ảnh bằng Imagen ({settings.IMAGEN_MODEL}): {e}")
            return None

ai_client = AIClient()
