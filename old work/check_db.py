import pandas as pd

df = pd.read_csv("./data/dataset.csv")


print(df.head())
print(df.shape)
print(df.info())


print("\nMissing values:")
print(df.isnull().sum())


# Duplicates
print("\nDuplicated rows:")
print(df.duplicated().sum())

print("\nDuplicated Order IDs:")
print(df["Order_ID"].duplicated().sum())


categorical_columns = [
    "Weather",
    "Traffic_Level",
    "Time_of_Day",
    "Vehicle_Type"
]

for column in categorical_columns:
    print(f"\n{column}")
    print(df[column].value_counts(dropna=False))

numerical_columns = [
    "Distance_km",
    "Preparation_Time_min",
    "Courier_Experience_yrs",
    "Delivery_Time_min"
]

print("\nNumerical description:")
print(df[numerical_columns].describe())

print("\nInvalid Distance:")
print((df["Distance_km"] <= 0).sum())

print("\nInvalid Preparation Time:")
print((df["Preparation_Time_min"] <= 0).sum())

print("\nInvalid Courier Experience:")
print((df["Courier_Experience_yrs"] < 0).sum())

print("\nInvalid Delivery Time:")
print((df["Delivery_Time_min"] <= 0).sum())

print(df["Delivery_Time_min"].describe())
print(df["Delivery_Time_min"].median())


import matplotlib.pyplot as plt

plt.hist(
    df["Delivery_Time_min"],
    bins=30,
    edgecolor="black"
)

plt.xlabel("Delivery Time (minutes)")
plt.ylabel("Frequency")
plt.title("Distribution of Delivery Time")

plt.show()

plt.boxplot(df["Delivery_Time_min"])

plt.ylabel("Delivery Time (minutes)")
plt.title("Boxplot of Delivery Time")

plt.show()

print(df["Delivery_Time_min"].skew())