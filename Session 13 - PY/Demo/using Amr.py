import pandas as pd
import numpy as np

print("--- Scores Series ---")
scores = pd.Series([90, 80, 70, 60, 50], index=['A', 'B', 'C', 'D', 'E'])
print(scores)

print("\n--- Accessing Specific Score (A) ---")
print(scores['A'])  # Accessing a specific score by index

print("\n--- Full DataFrame ---")
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
        'Age': [25, 30, 35, 40, 45]}
df = pd.DataFrame(data)
print(df)

print("\n--- Name Column Only ---")
print(df["Name"])

print("\n--- Data Count ---")
print(df.count())  # Accessing the count of rows in the DataFrame

print("\n--- Head (Default: First 5 rows) ---")
print(df.head()) # => All Data

print("\n--- First 2 rows ---")
print(df.head(2))

print("\n--- DataFrame Shape (Rows, Columns) ---")
print(df.shape)

print("\n--- Columns Names ---")
print(df.columns)

print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- Data Summary (Describe) ---")
print(df.describe())

print("\n--- Adding Salary Column ---")
df['Salary'] = [5000, 6000, 7000, 8000, 9500]
print(df)

print("\n--- Adding Bonus Column ---")
df['Bonus'] = df['Salary'] * 0.10
print(df)

print("\n--- Selecting Multiple Columns (Name & Age) ---")
print(df[["Name", "Age"]])

print("\n--- Accessing Row by Position (iloc) ---")
print(df.iloc[4])

print("\n--- Accessing Row by Label (loc) ---")
print(df.loc[4])

print("\n--- Set Name as Index & Get Bob's Row ---")
print(df.set_index("Name").loc["Bob"])

print("\n--- Set Name as Index & Get Bob's Age ---")
print(df.set_index("Name").loc["Bob", "Age"])

print("\n--- Filtering: People older than 30 ---")
print(df[df["Age"] > 30])

print("\n--- Filtering: Age > 30 AND Salary > 7000 ---")
print(df[((df["Age"] > 30 ) & (df["Salary"] > 7000))])

print("\n--- Sorting by Age (Ascending / Default) ---")
print(df.sort_values("Age"))

print("\n--- Sorting by Age (Descending) ---")
print(df.sort_values("Age", ascending=False))

print("\n--- Injecting a Missing Value (NaN) for Bob's Age ---")
df.loc[1, "Age"] = np.nan
print("Missing value added.")

print("\n--- Boolean Grid for Missing Values (True/False) ---")
print(df.isna())
print("-" * 30)
print(df)
print("-" * 30)

print("\n--- Checking Missing Values in 'Age' Column ---")
print(df["Age"].isna())

print("\n--- Counting Missing Values in 'Age' Column ---")
print(df["Age"].isna().sum())

print("\n--- Filling Missing Values with 0 ---")
print(df.fillna(0))

print("\n--- Dropping Rows with Missing Values ---")
print(df.dropna())

print("\n--- Grouping by Name: Count of Age ---")
print(df.groupby("Name")["Age"].count())

print("\n--- Grouping by Name: Max of Age ---")
print(df.groupby("Name")["Age"].max())

print("\n--- Grouping by Name: Mean of Age ---")
print(df.groupby("Name")["Age"].mean())

print("\n--- Grouping by Name: Multiple Aggregations (mean, max, count) ---")
print(df.groupby("Name")["Age"].agg(["mean", "max", "count"]))

print("\n--- Exporting Data to Excel and CSV ---")
df.to_excel('employees_data.xlsx', index=False)
df.to_csv('employees_data.csv', index=False)
print("Files saved successfully!")
