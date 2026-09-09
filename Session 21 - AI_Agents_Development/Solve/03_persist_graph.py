import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

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
        reply = "We apologize for the delay. We are tracking your package now."
    return {"draft": reply, "status": "drafted"}

def finalize_node(state: SupportState):
    return {"status": "ready"}

builder = StateGraph(SupportState)
builder.add_node("draft", draft_node)
builder.add_node("finalize", finalize_node)
builder.add_edge(START, "draft")
builder.add_edge("draft", "finalize")
builder.add_edge("finalize", END)

graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "ticket-1001"}}

result = graph.invoke(
    {"request": "My order is three days late", "draft": "", "status": "new"},
    config,
)

print("Thread result status:", result["status"])
print("Generated draft:", result["draft"])
