readings = [5, 10, 15, 20]
average = sum(readings) / len(readings)
print(f"Average reading: {average}") # => Average reading: 12.5
# --------------------------
total = 0
for batch_loss in [0.1, 0.2, 0.15, 0.05]:
    total += batch_loss
print(f"Total loss: {round(total, 2)}") # => Total loss: 0.5
# -------------------------
confidence = 0.87
is_flagged = False
should_alert = (confidence > 0.8) and (not is_flagged)
print(f"Should alert: {should_alert}") # => Should alert: True
# -------------------------
features = ['feature1', 'feature2', 'feature3']
for feature in features:
    print(f"Processing {feature}") # => Processing feature1
# -------------------------
config = {'learning_rate': 0.01, 'batch_size': 32, 'num_epochs': 10}
for key in config:
    print(f"{key}: {config[key]}") # => learning_rate: 0.01
for key, value in config.items():
    print(f"{key}: {value}") # => learning_rate: 0.01
# -------------------------
t = (1, 2, 3, 4)
for item in t:
    print(f"Processing {item}") # => Processing 1
# -------------------------
list_item = ["one", "two", "three", "four", "five"]
tuple_item = (1, 2, 3, 4, 5)
print(list_item.index("one"))  # => 0
print(list_item.index("three"))  # => 2
config = {}
for item in list_item:
    config[item] = tuple_item[list_item.index(item)]
print(config) # => {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
# -------------------------
def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
print(f"Average of readings: {calculate_average(readings)}") # => Average of readings: 12.5
# -------------------------
# A small, reusable preprocessing helper
def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)
print(normalize(75, 0, 100))  # => 0.75
