import os
from typing import TypedDict, Literal
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, interrupt

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
        reply = "Hello, we verified your order and it will arrive tomorrow."
    return {"draft": reply, "status": "drafted"}

def approval_node(state: SupportState) -> Command[Literal["send", "cancel"]]:
    approved = interrupt({
        "question": "Approve sending this support message to the customer?",
        "draft": state["draft"],
    })
    return Command(goto="send" if approved else "cancel")

def send_node(state: SupportState):
    print("Action executed: EMAIL SENT ->", state["draft"])
    return {"status": "sent"}

def cancel_node(state: SupportState):
    print("Action cancelled: EMAIL NOT SENT")
    return {"status": "cancelled"}

builder = StateGraph(SupportState)
builder.add_node("draft", draft_node)
builder.add_node("approval", approval_node)
builder.add_node("send", send_node)
builder.add_node("cancel", cancel_node)

builder.add_edge(START, "draft")
builder.add_edge("draft", "approval")
builder.add_edge("send", END)
builder.add_edge("cancel", END)

graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "ticket-2001"}}
initial_state = {"request": "My order is three days late", "draft": "", "status": "new"}

paused = graph.invoke(initial_state, config)
print("Graph Paused with Interrupt Payload:")
print(paused["__interrupt__"])

final = graph.invoke(Command(resume=True), config)
print("\nGraph Resumed with Approval (True):")
print("Final Status:", final["status"])
