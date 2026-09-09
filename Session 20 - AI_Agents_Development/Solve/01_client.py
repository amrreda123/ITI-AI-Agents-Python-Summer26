import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
assert api_key, "Missing GEMINI_API_KEY in environment or .env file"

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Reply with exactly: client ready",
)

print("Status:", response.text.strip())
