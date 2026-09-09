from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Mock Business Systems for n8n Agent")

SHEETS_DB = {
    "C-104": {"customer_id": "C-104", "order_id": 104, "status": "delayed", "total": 850, "balance": 1250},
    "C-205": {"customer_id": "C-205", "order_id": 205, "status": "shipped", "total": 420, "balance": 0},
}

class WebhookTicketPayload(BaseModel):
    ticket_id: str
    customer_id: str
    message: str

@app.get("/api/sheets/lookup/{customer_id}")
def lookup_customer(customer_id: str):
    customer = SHEETS_DB.get(customer_id.upper())
    if not customer:
        raise HTTPException(status_code=404, detail="Customer record not found in Google Sheets")
    return customer

@app.post("/webhook-test/agent-support")
def simulate_agent_support(payload: WebhookTicketPayload):
    customer_info = SHEETS_DB.get(payload.customer_id.upper())
    if customer_info:
        msg = f"Order #{customer_info['order_id']} for customer {payload.customer_id} is currently {customer_info['status']}. Total is {customer_info['total']} EGP."
    else:
        msg = f"No live record found for customer {payload.customer_id}."

    return {
        "ticket_id": payload.ticket_id,
        "status": "processed",
        "message": msg
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
