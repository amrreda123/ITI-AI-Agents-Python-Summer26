from typing import Literal
from pydantic import BaseModel, Field

class OrderLookup(BaseModel):
    order_id: int = Field(gt=0)

class ShippingQuote(BaseModel):
    weight_kg: float = Field(gt=0, le=100)
    zone: Literal["local", "regional", "international"] = Field(default="local")

def get_order(order_id: int) -> dict:
    db = {
        101: {"status": "delivered", "weight_kg": 1.5, "total": 250, "zone": "local"},
        104: {"status": "delayed", "weight_kg": 4.2, "total": 850, "zone": "regional"},
        105: {"status": "processing", "weight_kg": 0.8, "total": 120, "zone": "local"}
    }
    return db.get(order_id, {"status": "not_found", "message": f"Order {order_id} does not exist."})

def calculate_shipping(weight_kg: float, zone: str = "local") -> dict:
    rates = {
        "local": 20.0,
        "regional": 35.0,
        "international": 120.0
    }
    rate_per_kg = rates.get(zone.lower(), 50.0)
    total_cost = round(weight_kg * rate_per_kg, 2)
    return {
        "weight_kg": weight_kg,
        "zone": zone.lower(),
        "cost": total_cost,
        "currency": "EGP"
    }

if __name__ == "__main__":
    order_args = OrderLookup(order_id=104).model_dump()
    print(get_order(**order_args))

    ship_args = ShippingQuote(weight_kg=4.2, zone="regional").model_dump()
    print(calculate_shipping(**ship_args))
