canFly = False
bird = "sparrow" if canFly else "Penguin"
print(bird) #=> Penguin
# ------------------------------
json_data = ":".join(["name", "age", "city"])
print(json_data) # => name:age:city
name_data = " ".join("Amr")
print(name_data) # => A m r
# ------------------------------
name_parts = "Amr Reda".split(" ")
print(name_parts) # => ['Amr', 'Reda']
django_parts = "django:flask".split(":")
print(django_parts) # => ['django', 'flask']
# ------------------------------
print(list("Amr")) # => ['A', 'm', 'r']
# ------------------------------
x = 10
y = 20
print(f"x = {x}, y = {y}") # => x = 10, y = 20
temp = x
x = y
y = temp
print(f"x = {x}, y = {y}") # => x = 20, y = 10
x, y = y, x
print(f"x = {x}, y = {y}") # => x = 20, y = 10
# -----------------------------
l = [1, 2, 3, 4, 5]
print(all(x > 0 for x in l))  # True
print(any(x > 3 for x in l))  # True
