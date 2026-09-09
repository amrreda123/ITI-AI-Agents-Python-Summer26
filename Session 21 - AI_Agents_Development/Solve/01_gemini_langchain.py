import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

try:
    response = model.invoke("Reply with: model ready")
    print(response.content)
except Exception as e:
    print("Connection status:", e)
