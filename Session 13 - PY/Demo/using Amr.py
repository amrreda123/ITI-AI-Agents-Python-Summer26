import pandas as pd

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

# print(df[["Name", "age"]])
print(df.iloc(1))

# print("--- People older than 30 ---")
# # هنا بنعمل الفلترة
# older_than_30 = df[df['Age'] > 30]
# print(older_than_30)
# print("--- Adding Salary Column ---")
# # إضافة عمود المرتبات
# df['Salary'] = [5000, 6000, 7000, 8000, 9500]
# print(df)
# print("--- Adding Bonus Column ---")
# # حساب المكافأة بضرب عمود المرتب في 0.10
# df['Bonus'] = df['Salary'] * 0.10
# print(df)
# df.to_excel('employees_data.xlsx', index=False)
# df.to_csv('employees_data.csv', index=False)
