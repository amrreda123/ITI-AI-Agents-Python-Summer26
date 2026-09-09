import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_order(order_id: int) -> dict:
    db = {104: {"status": "delayed", "weight_kg": 4.2, "total": 850, "zone": "regional"}}
    return db.get(order_id, {"status": "not_found"})

def calculate_shipping(weight_kg: float, zone: str = "local") -> dict:
    rates = {"local": 20.0, "regional": 35.0, "international": 120.0}
    return {"cost": weight_kg * rates.get(zone.lower(), 50.0), "currency": "EGP"}

config = types.GenerateContentConfig(
    tools=[get_order, calculate_shipping],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

prompt = "What is the current status of order 104?"

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config,
    )

    candidate = response.candidates[0]
    call = candidate.content.parts[0].function_call

    if call:
        print("Function Name:", call.name)
        print("Arguments:", call.args)
    else:
        print(response.text)

except Exception as e:
    print(e)
