import os
from metrics_toolkit.my_functions import sum_values, subtract_values, divide_values, multiply_values

path = os.path.dirname(os.path.abspath(__file__))
print("--- 01 Load Sensor Readings into a List ---")
readings = []
with open(os.path.join(path, "sensor_log.txt"), "r") as fp:
    for line in fp:
        readings.append(line.strip())
print(readings)
# -----------------------------------------------------------
print("\n--- 02 Save a List of Model Names to Disk ---")
model_names = ["logistic_regression", "random_forest", "svm"]
model_names.append("Amr")

with open(os.path.join(path, "model_registry.txt"), "w") as fp:
    for name in model_names:
        fp.write(name + "\n")
print("Model names saved to model_registry.txt successfully.")
# -----------------------------------------------------------
print("\n--- 04 Build a Calculator on Top of Your Package ---")

def run_calculator():
    try:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        operand = int(input("0=sum, 1=subtract, 2=divide, 3=multiply: "))
        
        if operand == 0:
            print(sum_values(a, b))
        elif operand == 1:
            if a == 0 or b == 0:
                raise ValueError("subtracting zero from Number")
            print(subtract_values(a, b))
        elif operand == 2:
            if a == 0 or b == 0:
                raise ZeroDivisionError("can't divide with zero")
            print(divide_values(a, b))
        elif operand == 3:
            if a == 0 or b == 0:
                raise ValueError("Multiply with Zero")
            print(multiply_values(a, b))
    except (ValueError, ZeroDivisionError) as e:
        print(f"Invalid operation: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_calculator()
