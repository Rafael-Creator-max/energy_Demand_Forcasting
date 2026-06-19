import pandas as pd 

print("Pandas werkt!")
print(pd.__version__)

df = pd.read_csv("../data/monthly_hourly_load_values_2019.csv",sep="\t")

print(df.head())
print("\nKolommen:")
print(df.columns)

print("\nInfo:")
print(df.info())

with open("../data/monthly_hourly_load_values_2019.csv", "r", encoding="utf-8") as f:
    line = f.readline()

print(repr(line))

print(df["CountryCode"].unique())

