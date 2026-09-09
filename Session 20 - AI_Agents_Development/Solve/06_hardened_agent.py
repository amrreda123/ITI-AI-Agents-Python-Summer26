import os
import time
from typing import Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class OrderLookupSchema(BaseModel):
    order_id: int = Field(gt=0)

class ShippingQuoteSchema(BaseModel):
    weight_kg: float = Field(gt=0, le=100)
    zone: Literal["local", "regional", "international"] = Field(default="local")

def get_order(order_id: int) -> dict:
    database = {
        101: {"order_id": 101, "status": "delivered", "weight_kg": 1.2, "zone": "local", "total": 320},
        104: {"order_id": 104, "status": "delayed", "weight_kg": 4.5, "zone": "regional", "total": 850},
        108: {"order_id": 108, "status": "in_transit", "weight_kg": 12.0, "zone": "international", "total": 2400},
    }
    if order_id not in database:
        return {"error": "Not Found", "message": f"Order {order_id} does not exist in the database."}
    return database[order_id]

def calculate_shipping(weight_kg: float, zone: str = "local") -> dict:
    rates = {"local": 20.0, "regional": 35.0, "international": 120.0}
    zone_clean = zone.lower()
    if zone_clean not in rates:
        return {"error": "Invalid Zone", "message": f"Zone must be one of {list(rates.keys())}"}
    
    total = round(weight_kg * rates[zone_clean], 2)
    return {"weight_kg": weight_kg, "zone": zone_clean, "shipping_cost": total, "currency": "EGP"}

REGISTRY = {
    "get_order": {"func": get_order, "schema": OrderLookupSchema},
    "calculate_shipping": {"func": calculate_shipping, "schema": ShippingQuoteSchema},
}

config = types.GenerateContentConfig(
    tools=[get_order, calculate_shipping],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    temperature=0.2,
)

def execute_safe_tool(tool_name: str, raw_args: dict) -> dict:
    if tool_name not in REGISTRY:
        return {"error": "Unauthorized", "message": f"Tool '{tool_name}' is not in the whitelist."}

    tool_info = REGISTRY[tool_name]
    schema = tool_info["schema"]
    func = tool_info["func"]

    try:
        validated_args = schema(**raw_args).model_dump()
    except ValidationError as val_err:
        return {"error": "Validation Error", "details": str(val_err)}

    try:
        start_time = time.time()
        result = func(**validated_args)
        duration_ms = round((time.time() - start_time) * 1000, 2)
        print(f"[Log] Executed {tool_name} in {duration_ms}ms")
        return result
    except Exception as exc:
        print(f"[Log] Tool execution failed: {exc}")
        return {"error": "Execution Failure", "details": str(exc)}

def hardened_agent_loop(query: str, max_steps: int = 5):
    contents = [types.Content(role="user", parts=[types.Part(text=query)])]

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
            print(response.text.strip())
            return response.text

        observation = execute_safe_tool(call.name, dict(call.args))

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
        print(f"Agent stopped: reached MAX_STEPS ({max_steps}) guard limit.")

if __name__ == "__main__":
    test_query = "What is the status of order 104, and how much will it cost to ship it?"
    try:
        hardened_agent_loop(test_query)
    except Exception as e:
        print(e)
