from google import genai
import os
import json
import base64
from .base import PoolDetector

class LlmDetector(PoolDetector):
    def __init__(self, model_name="gemini-1.5-pro-002"):  
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = model_name

    def detect(self, image_path: str):
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        prompt = """Analyze this aerial image...
        Return ONLY valid JSON..."""   

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    {"role": "user", "parts": [
                        {"inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base64.b64encode(image_bytes).decode("utf-8")
                        }},
                        {"text": prompt}
                    ]}
                ],
                generation_config={"temperature": 0.2, "response_mime_type": "application/json"}
            )

            text = response.candidates[0].content.parts[0].text.strip()

            # Clean up markdown if present
            if text.startswith("```json"):
                text = text.split("```json", 1)[1].split("```")[0].strip()

            data = json.loads(text)
            if data.get("found", False):
                coords = data.get("coordinates", [])
                return [(int(x), int(y)) for x, y in coords]

        except Exception as e:
            print(f"LLM error: {e}")
            return []

        return []