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

TOOLS = {
    "get_order": get_order,
    "calculate_shipping": calculate_shipping,
}

config = types.GenerateContentConfig(
    tools=[get_order, calculate_shipping],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

user_query = "What is the status of order 104?"
contents = [
    types.Content(role="user", parts=[types.Part(text=user_query)])
]

try:
    response1 = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config,
    )

    part = response1.candidates[0].content.parts[0]
    call = part.function_call

    if call:
        if call.name not in TOOLS:
            raise ValueError(f"Blocked unapproved tool: {call.name}")
        
        result = TOOLS[call.name](**call.args)

        contents.append(response1.candidates[0].content)
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_function_response(
                name=call.name,
                response={"result": result},
                id=call.id,
            )]
        ))

        final_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        )
        print(final_response.text)

except Exception as e:
    print(e)
