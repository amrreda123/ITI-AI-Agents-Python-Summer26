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
    return {
        "draft": f"Hello, regarding your request '{state['request']}', our team is on it.",
        "status": "drafted"
    }

def approval_node(state: SupportState) -> Command[Literal["send", "cancel"]]:
    feedback = interrupt({
        "question": "Review message. Approve, reject, or edit draft.",
        "current_draft": state["draft"]
    })
    
    if isinstance(feedback, dict) and feedback.get("approved"):
        updated_draft = feedback.get("edited_draft", state["draft"])
        return Command(goto="send", update={"draft": updated_draft})
    elif feedback is True:
        return Command(goto="send")
    else:
        return Command(goto="cancel")

def send_node(state: SupportState):
    print("Email sent to user with content:", state["draft"])
    return {"status": "sent"}

def cancel_node(state: SupportState):
    print("Action was rejected by human reviewer.")
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

print("=== Test 1: Rejection Path ===")
config_reject = {"configurable": {"thread_id": "ticket-reject-101"}}
graph.invoke({"request": "I want a full refund immediately", "draft": "", "status": "new"}, config_reject)
rejected_result = graph.invoke(Command(resume=False), config_reject)
print("Status after reject:", rejected_result["status"])

print("\n=== Test 2: Edit & Approve Path ===")
config_edit = {"configurable": {"thread_id": "ticket-edit-102"}}
graph.invoke({"request": "My item is delayed", "draft": "", "status": "new"}, config_edit)
edited_result = graph.invoke(Command(resume={"approved": True, "edited_draft": "Your item has been dispatched and will arrive today."}), config_edit)
print("Status after edit & approve:", edited_result["status"])
print("Final Sent Draft:", edited_result["draft"])
