import pandas as pd

# 01 Build Your First DataFrame
print("--- 01 Build Your First DataFrame ---")
data = {
    "name": ["Amir", "Sara", "Leo", "Nina"],
    "quiz1": [90, 70, 82, 60],
    "quiz2": [85, 60, 77, 55]
}
df = pd.DataFrame(data)
print(df)

# 02 Explore the Table
print("\n--- 02 Explore the Table ---")
print("Shape:", df.shape)
print("Columns:", df.columns)
print("Data Types:\n", df.dtypes)
print("Describe:\n", df.describe())

# 03 Select Rows and Columns
print("\n--- 03 Select Rows and Columns ---")
print("quiz1 column:\n", df["quiz1"])
print("name and quiz1 columns:\n", df[["name", "quiz1"]])

df2 = df.set_index("name")
print("loc['Leo']:\n", df2.loc["Leo"])
print("iloc[2]:\n", df2.iloc[2])

# 04 Filter and Sort
print("\n--- 04 Filter and Sort ---")
top = df[df["quiz1"] >= 80]
print("Top (quiz1 >= 80):\n", top)

print("Sorted by quiz1 (descending):\n", df.sort_values("quiz1", ascending=False))

both_above_70 = df[(df["quiz1"] >= 70) & (df["quiz2"] >= 70)]
print("quiz1 >= 70 & quiz2 >= 70:\n", both_above_70)

# 05 Add a Column and Handle a Gap
print("\n--- 05 Add a Column and Handle a Gap ---")
df["average"] = (df["quiz1"] + df["quiz2"]) / 2
df["passed"] = df["average"] >= 70
print(df[["name", "average", "passed"]])

df.loc[1, "quiz2"] = None
print("Missing values per column:\n", df.isna().sum())

filled = df.fillna(0)
print("Filled with 0:\n", filled)

dropped = df.dropna()
print("Dropped missing:\n", dropped)

# Bonus Stretch Goal
print("\n--- Bonus Stretch Goal ---")
df["study_group"] = ["A", "B", "A", "B"]

print("Average quiz1 by group:\n", df.groupby("study_group")["quiz1"].mean())
print("Fuller summary by group:\n", df.groupby("study_group")["quiz1"].agg(["mean", "max", "count"]))

df.to_csv("class_results.csv", index=False)
read_back_df = pd.read_csv("class_results.csv")
print("Read back from CSV:\n", read_back_df)
