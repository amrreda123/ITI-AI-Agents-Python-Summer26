# ------------------------------------------
# 01 Identifier & Variable Roll Call
# ------------------------------------------
print("--- 01 Identifier & Variable Roll Call ---")
model_name = "AlphaNet"
accuracy = 0.95
is_deployed = True
version_number = 2

print(f"model_name: {model_name}, type: {type(model_name)}")
print(f"accuracy: {accuracy}, type: {type(accuracy)}")
print(f"is_deployed: {is_deployed}, type: {type(is_deployed)}")
print(f"version_number: {version_number}, type: {type(version_number)}\n")

# ------------------------------------------
# 02 Type Conversion Station
# ------------------------------------------
print("--- 02 Type Conversion Station ---")
raw_accuracy = "94.7"
raw_epochs = "10"

accuracy_float = float(raw_accuracy)
epochs_int = int(raw_epochs)

print(f"The model trained for {epochs_int} epochs and achieved an accuracy of {accuracy_float}%.\n")

# ------------------------------------------
# 03 Operators Workout
# ------------------------------------------
print("--- 03 Operators Workout ---")
x = 17
y = 5

print(f"x + y = {x + y}")
print(f"x - y = {x - y}")
print(f"x * y = {x * y}")
print(f"x / y = {x / y}")
print(f"x % y = {x % y}")
print(f"x ** y = {x ** y}")
print(f"x // y = {x // y}")

total = 0
total += 5
print(f"total after += 5: {total}")
total -= 2
print(f"total after -= 2: {total}")
total *= 3
print(f"total after *= 3: {total}\n")

# ------------------------------------------
# 04 String Toolbox
# ------------------------------------------
print("--- 04 String Toolbox ---")
model_name_raw = " GPT-4 "
cleaned_name = model_name_raw.strip().upper().replace("-", "_")

print(f"Cleaned string: '{cleaned_name}'")
print(f"Length: {len(cleaned_name)}")
print(f"First three characters: '{cleaned_name[:3]}'\n")

# ------------------------------------------
# 05 List Lab
# ------------------------------------------
print("--- 05 List Lab ---")
scores = [0.71, 0.85, 0.63, 0.90, 0.78]
scores.append(0.82)
scores[0] = 0.75

print(f"Last three scores: {scores[-3:]}")
print(f"List length: {len(scores)}\n")

# ------------------------------------------
# 06 Tuple Vault
# ------------------------------------------
print("--- 06 Tuple Vault ---")
image_shape = (224, 224, 3)
print(f"Height: {image_shape[0]}")
print(f"Width: {image_shape[1]}")
print(f"Channels: {image_shape[2]}")
print()

# ------------------------------------------
# 07 Dictionary Depot
# ------------------------------------------
print("--- 07 Dictionary Depot ---")
config = {'learning_rate': 0.001, 'batch_size': 32}
config['epochs'] = 10
config['batch_size'] = 64

print(f"Whole dictionary: {config}")
print(f"Keys: {config.keys()}")
print(f"Values: {config.values()}\n")

# ------------------------------------------
# 08 Mini Challenge — Model Report Card
# ------------------------------------------
print("--- 08 Mini Challenge ---")
report = {
    'name': 'QuantumStride', 
    'accuracy': 0.912, 
    'metrics': {'precision': 0.89, 'recall': 0.87}, 
    'sample_predictions': [0.81, 0.42, 0.95]
}

print(f"Model name: {report['name']}")
print(f"Precision: {report['metrics']['precision']}")
print(f"Second sample prediction: {report['sample_predictions'][1]}\n")

# ------------------------------------------
# Quick Practice — Warm-up Problems
# ------------------------------------------
print("--- Quick Practice ---")
# 1. Add two numbers
num1, num2 = 10, 20
print(f"Sum of {num1} and {num2} = {num1 + num2}")

# 2. Swap without third variable
a, b = 5, 10
a, b = b, a
print(f"Swapped: a={a}, b={b}")

# 3. Reverse string
s = "Python"
print(f"Reversed '{s}': {s[::-1]}")

# 4. Convert list to tuple and back
my_list = [1, 2, 3]
my_tuple = tuple(my_list)
back_to_list = list(my_tuple)
print(f"Original list: {my_list}, as tuple: {my_tuple}, back to list: {back_to_list}")
