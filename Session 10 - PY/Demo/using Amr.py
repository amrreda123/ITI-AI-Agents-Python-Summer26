numbers = ["10", "5", "0", "oops", "2"]
for n in numbers:
    try:
        result = 100 / int(n)
    except ValueError as e:
        print(n, "-> not a number => " , e)
    except ZeroDivisionError as e:
        print(n, "-> can't divide by zero => " , e)
    else:
        print(n, "-> 100 /", n, "=", result)
    finally:
            print("  checked", n)
print("-------" * 10)
# -----------------------------
def check_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    elif age < 18:
        return "Minor"
    else:
        return "Adult"
ages = [15, 20, -5, 30]
for age in ages:
    try:
        status = check_age(age)
        print(f"Age {age}: {status}")
    except ValueError as e:
        print(f"Age {age}: Error - {e}")
print("-------" * 10)
# -----------------------------
fl = open("employees_data.csv", "r")
print("--- Full Content ---")
print(fl.read())
fl.seek(0) # Move the file pointer back to the beginning of the file
print("--- Read 4 Characters ---")
print(fl.read(4))
fl.seek(0)
print("--- Read 1 Line ---")
print(fl.readline())
print("--- Read Another Line ---")
print(fl.readline())
fl.seek(0)
print("--- Read All Lines into a List ---")
for line in fl:
    print(line.split(","))
print("--- Read All Lines into a List using readlines() ---")
fl.seek(0)
print(fl.readlines())
fl.close()
print("-------" * 10)
# -----------------------------
fl = open("running_log.txt", "w")
for i in range(50):
        fl.write(f"epoch={i+1:<2} => loss={round(0.842*(i+1), 3)}\n") # f-string formatting with left alignment and rounding
fl.close()
with open("dataset.txt", "w") as fl:
    for i in range(100):
        fl.write(f"data_point_{i+1}\n")
print("-------" * 10)
# ------------------------------
import os
os.remove("dataset.txt") if os.path.exists("dataset.txt") else None
print("\n--- File Operations ---\n")
print(os.getcwd()) # Get the current working directory
print("\n--- List Files and Directories ---\n")
print(os.listdir()) # List all files and directories in the current working directory
print("\n--- Absolute Path of a File ---\n")
print(os.listdir("Session 10 - PY")) # List all files and directories in the current working directory
print("\n--- Check if a File Exists ---\n")
print(os.path.abspath("running_log.txt")) # Get the absolute path of the file
print("\n--- Check if a File Exists ---\n")
print(os.path.exists("running_log.txt")) # Check if the file exists
print("\n--- Check if a Directory Exists ---\n")
print(os.path.exists("Session 10 - PY")) # Check if the directory exists
print("\n--- Check if a Path is a File ---\n")
print(os.path.isfile("running_log.txt")) # Check if the path is a file
print("\n--- Check if a Path is a Directory ---\n")
print(os.path.isdir("Session 10 - PY")) # Check if the path is a directory
print("\n--- Get File Size ---\n")
print(os.path.getsize("running_log.txt")) # Get the size of the file in bytes
print("\n--- Get File Creation Time ---\n")
print(os.path.getctime("running_log.txt")) # Get the creation time of the file
print(os.path.join("Session 10 - PY", "employees_data.csv"))
print(os.mkdir("Models"))
print(os.makedirs("outputs/saved_models/v1"))
print(os.rename("running_log.txt", "training_history.txt"))
os.path.basename("Session 10 - PY/employees_data.csv")
os.path.dirname("Session 10 - PY/employees_data.csv")
print("----" * 10)
# ---------------------------
import math
import re
# ---------------------------
import numpy as np
arr = np.array([1, 2, 3])
print(arr.mean())
# ---------------
# Pythonic
scores = [0.91, 0.87, 0.94, 0.88]
a, b, c, d = scores
print(f"a => {a}")
print(f"a => {b}")
print(f"a => {c}")
print(f"a => {d}")
print("----" * 10)
first, *rest = scores
print(first)
print(rest)
print("----" * 10)
squares = [i * i for i in range(10)]
print(squares)
print("----" * 10)
keys = ["epoch", "loss", "accuracy"]
values = [1, 0.842, 0.91]
for k, v in zip(keys, values):
    print(f"{k}: {v}")
print("----" * 10)
def normalize_data(raw_features):
    min_val = min(raw_features)
    max_val = max(raw_features)
    return [(x - min_val) / (max_val - min_val) for x in raw_features]
my_data = [100, 200, 150, 500, 50]
result = normalize_data(my_data)
print(result)
print("----" * 10)
# Normal function
def double(x):
    return x + x
# Equivalent lambda arguments: expression
double = lambda x: x + x
print("----" * 10)
