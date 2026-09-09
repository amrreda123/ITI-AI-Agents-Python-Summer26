def calculate_total_price(subtotal: float, tax_rate: float = 0.08) -> float:
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative")
    tax_amount = subtotal * tax_rate
    return round(subtotal + tax_amount, 2)


def format_user_summary(user_data: dict) -> str:
    name = user_data.get("name", "Unknown User")
    role = user_data.get("role", "Guest")
    email = user_data.get("email", "N/A")
    return f"User: {name} | Role: {role} | Contact: {email}"


def filter_high_rated_items(items: list[dict], min_rating: float = 4.5) -> list[dict]:
    return [item for item in items if item.get("rating", 0) >= min_rating]


if __name__ == "__main__":
    total = calculate_total_price(100.0)
    print(f"Total with 8% tax: ${total}")
    
    sample_user = {"name": "Amr Reda", "role": "AI Engineer", "email": "amr@example.com"}
    print(format_user_summary(sample_user))
