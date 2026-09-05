from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

stream = client.models.generate_content_stream(
    model="gemini-3.7-flash",
    contents="Write a short poem about the ocean."
)

for chunk in stream:
    if chunk.text:
        print(chunk.text, end="", flush=True)
print()
