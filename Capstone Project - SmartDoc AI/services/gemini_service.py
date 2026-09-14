import json
import logging
from google import genai
from google.genai import types
from pydantic import ValidationError

from settings import settings
from schemas import AIAnalysisResponse

logger = logging.getLogger("smartdoc.gemini_service")


def get_gemini_client() -> genai.Client:
    api_key = settings.GEMINI_API_KEY
    if not api_key or api_key == "replace_me":
        raise ValueError("GEMINI_API_KEY is not configured in environment or .env file.")
    return genai.Client(api_key=api_key)


def build_rtcf_prompt(document_content: str) -> str:
    return f"""### ROLE
You are a careful document analyst.

### TASK
Summarize and classify the supplied document accurately.

### CONTEXT
Use ONLY the provided document content below. Do not assume or invent missing facts:
<DOCUMENT_CONTENT>
{document_content}
</DOCUMENT_CONTENT>

### FORMAT
Return valid JSON matching this schema:
{{
  "summary": "Concise 1-3 sentence summary of the document",
  "key_points": ["Key point 1", "Key point 2", ...],
  "category": "technical" | "business" | "general",
  "suggested_priority": 1 to 5 (integer, where 5 is highest)
}}
"""


def analyze_document_content(content: str) -> AIAnalysisResponse:
    try:
        client = get_gemini_client()
        prompt = build_rtcf_prompt(content)

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AIAnalysisResponse,
                temperature=0.2,
            ),
        )

        raw_text = response.text or "{}"
        parsed = json.loads(raw_text)
        return AIAnalysisResponse(**parsed)

    except (ValueError, ValidationError, json.JSONDecodeError) as err:
        logger.error(f"Analysis parsing error: {err}")
        raise RuntimeError("Failed to process document analysis structured output.")
    except Exception as err:
        logger.error(f"Gemini API invocation error: {type(err).__name__}")
        raise RuntimeError("Upstream AI analysis service is currently unavailable.")
