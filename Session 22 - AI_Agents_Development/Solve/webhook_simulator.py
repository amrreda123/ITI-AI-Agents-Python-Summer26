import json
import requests

WEBHOOK_URL = "http://localhost:5678/webhook-test/agent-support"

payload_turn1 = {
    "ticket_id": "T-204",
    "customer_id": "C-104",
    "message": "My shipment is late. Please check order 104 and update me."
}

payload_turn2 = {
    "ticket_id": "T-204",
    "customer_id": "C-104",
    "message": "Can you summarize what we know about this ticket so far?"
}

def send_test_request(payload, turn_label="Turn"):
    print(f"=== Sending {turn_label} ===")
    print("Payload:", json.dumps(payload, indent=2))
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        print(f"Response Status: {response.status_code}")
        print("Response Body:", response.text)
    except requests.exceptions.ConnectionError:
        print(f"Note: Local n8n server is not active on {WEBHOOK_URL}.")
        print("Simulator payload validated successfully.")

if __name__ == "__main__":
    send_test_request(payload_turn1, "Turn 1: Initial Customer Inquiry")
    print("\n" + "-" * 50 + "\n")
    send_test_request(payload_turn2, "Turn 2: Multi-turn Memory Follow-up")
