import pandas as pd

# dataframe = pd.read_csv("./data/dataset.csv")
# print(dataframe.head())
# print(dataframe.shape)
# print(dataframe.columns)
# print(dataframe.info())

# print(dataframe.isna().sum())

# print(dataframe["Time_of_Day"].value_counts(dropna=False))
# print(dataframe["Traffic_Level"].value_counts(dropna=False))
# print(dataframe["Weather"].value_counts(dropna=False))

# dataframe["Weather"] = dataframe["Weather"].fillna(dataframe["Weather"].mode()[0])
# dataframe["Traffic_Level"] = dataframe["Traffic_Level"].fillna(
#     dataframe["Traffic_Level"].mode()[0]
# )
# dataframe["Time_of_Day"] = dataframe["Time_of_Day"].fillna(
#     dataframe["Time_of_Day"].mode()[0]
# )
# dataframe["Courier_Experience_yrs"] = dataframe["Courier_Experience_yrs"].fillna(
#     dataframe["Courier_Experience_yrs"].median()
# )
# print((dataframe["Distance_km"] < 0).sum())
# print((dataframe["Distance_km"] == 0).sum())
# print(dataframe["Courier_Experience_yrs"].describe())

# print("Duplicated rows:", dataframe.duplicated().sum())

# print("Duplicated Order_ID:", dataframe["Order_ID"].duplicated().sum())

# print("Invalid distance:")
# print((dataframe["Distance_km"] <= 0).sum())

# print("Invalid preparation time:")
# print((dataframe["Preparation_Time_min"] <= 0).sum())

# print("Invalid courier experience:")
# print((dataframe["Courier_Experience_yrs"] < 0).sum())

# print("Invalid delivery time:")
# print((dataframe["Delivery_Time_min"] <= 0).sum())

# categorical_columns = [
#     "Weather",
#     "Traffic_Level",
#     "Time_of_Day",
#     "Vehicle_Type"
# ]

# for column in categorical_columns:
#     print(f"\n{column}")
#     print(dataframe[column].value_counts(dropna=False))


df = pd.read_csv("./data/food-delivery.csv")

print(df.info())