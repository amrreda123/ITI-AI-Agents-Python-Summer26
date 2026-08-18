import numpy as np

print("--- 01 Build Your First Array ---")
scores_list = [78, 85, 92, 60, 88]
scores_array = np.array(scores_list)

print(scores_array)
print(scores_array.shape)
print(scores_array.dtype)

# -----------------------------------------------------------
print("\n--- 02 A Whole Class of Scores ---")
quiz_grid = np.array([
    [90, 85, 78, 92],
    [70, 88, 95, 60],
    [82, 77, 91, 84]
])

print(quiz_grid)
print(quiz_grid.shape)
print(quiz_grid.ndim)
print(quiz_grid[0])
print(quiz_grid[0, 2])

# -----------------------------------------------------------
print("\n--- 03 Slice Out Rows and Columns ---")
print(quiz_grid[0:2])
print(quiz_grid[:, 0])
print(quiz_grid[-1, -1])

# -----------------------------------------------------------
print("\n--- 04 Grade with Math ---")
quiz_grid[:, 2] += 5

print(quiz_grid)
print(quiz_grid.mean(axis=1))
print(quiz_grid.max(axis=1))

# -----------------------------------------------------------
print("\n--- 05 Find Who Passed ---")
averages = quiz_grid.mean(axis=1)
passed = averages >= 80
print(passed)
print(averages[passed])
print(f"Number who passed: {passed.sum()}")
