import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_order(order_id: int) -> dict:
    db = {
        104: {"order_id": 104, "status": "delayed", "weight_kg": 4.2, "zone": "regional", "total": 850}
    }
    return db.get(order_id, {"status": "not_found"})

def calculate_shipping(weight_kg: float, zone: str = "local") -> dict:
    rates = {"local": 20.0, "regional": 35.0, "international": 120.0}
    cost = round(weight_kg * rates.get(zone.lower(), 50.0), 2)
    return {"weight_kg": weight_kg, "zone": zone, "shipping_cost": cost, "currency": "EGP"}

TOOLS = {
    "get_order": get_order,
    "calculate_shipping": calculate_shipping,
}

config = types.GenerateContentConfig(
    tools=[get_order, calculate_shipping],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

def run_agent(user_prompt: str, max_steps: int = 5):
    contents = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    for step in range(1, max_steps + 1):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        )

        candidate = response.candidates[0]
        part = candidate.content.parts[0]
        call = part.function_call

        if not call:
            print(response.text)
            return response.text

        if call.name not in TOOLS:
            raise ValueError(f"Blocked unauthorized tool call: {call.name}")

        tool_func = TOOLS[call.name]
        observation = tool_func(**call.args)

        contents.append(candidate.content)
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_function_response(
                name=call.name,
                response={"result": observation},
                id=call.id,
            )]
        ))
    else:
        raise RuntimeError(f"Agent exceeded safety limit of {max_steps} steps without terminating.")

if __name__ == "__main__":
    prompt = "Check order 104, find its weight and zone, and calculate its shipping cost."
    try:
        run_agent(prompt)
    except Exception as e:
        print(e)
