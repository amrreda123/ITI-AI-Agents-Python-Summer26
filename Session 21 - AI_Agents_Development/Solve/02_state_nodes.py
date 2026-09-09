import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

class SupportState(TypedDict):
    request: str
    draft: str
    status: str

def draft_node(state: SupportState):
    prompt = f"Draft a concise support response for: {state['request']}"
    try:
        reply = model.invoke(prompt).content
    except Exception:
        reply = "Thank you for reaching out. We are investigating your late order."
    return {"draft": reply, "status": "drafted"}

def finalize_node(state: SupportState):
    return {"status": "ready"}

if __name__ == "__main__":
    initial = {"request": "My order is 3 days late", "draft": "", "status": "new"}
    drafted = draft_node(initial)
    print("Draft Node Output:", drafted)
    final = finalize_node(drafted)
    print("Finalize Node Output:", final)
