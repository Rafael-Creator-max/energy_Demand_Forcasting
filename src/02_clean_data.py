import pandas as pd

df = pd.read_csv("../data/processed/all_load_values.csv"
    ,low_memory=False
    )

be_df = df[df["CountryCode"] == "BE"].copy()

#Transform str to timestamp
be_df["DateUTC"] = pd.to_datetime(
    be_df["DateUTC"],
    format="mixed",
    dayfirst=True
)

#Chronologic order
be_df = be_df.sort_values("DateUTC")

#Set new columns 
be_df["Hour"] = be_df["DateUTC"].dt.hour
be_df["Month"] = be_df["DateUTC"].dt.month
be_df["DayOfWeek"] = be_df["DateUTC"].dt.dayofweek
be_df["Year"] = be_df["DateUTC"].dt.year

#Take only the colummns we need
be_df = be_df[[
    "DateUTC",
    "CountryCode",
    "Value",
    "Hour",
    "DayOfWeek",
    "Month",
    "Year"
]]



be_df.to_csv("../data/processed/belgium_load_clean.csv", index=False)

print("Clean Belgium dataset saved.")
print(be_df.head())
print(be_df.shape)

#Test 1
print(be_df["Year"].unique())