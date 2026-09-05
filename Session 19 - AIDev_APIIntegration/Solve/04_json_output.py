import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

def summarize(text):
    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=(
                "Summarize the text. Return JSON with a summary string and a "
                "key_points array of strings."
            ),
            response_mime_type="application/json"
        )
    )
    return json.loads(response.text)

result = summarize("Artificial intelligence (AI) is intelligence demonstrated by machines, unlike the natural intelligence displayed by humans and animals, which involves consciousness and emotionality.")
print(result["summary"])
for point in result["key_points"]:
    print("-", point)
