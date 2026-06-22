import pandas as pd 
import matplotlib.pyplot as plt


print("Pandas werkt!")
print(pd.__version__)

print("--------------------------------")


df = pd.read_csv("../data/monthly_hourly_load_values_2019.csv",sep="\t")

print(df.head())
print("\nKolommen:")
print(df.columns)

print("--------------------------------")

print("\nInfo:")
print(df.info())

with open("../data/monthly_hourly_load_values_2019.csv", "r", encoding="utf-8") as f:
    line = f.readline()

print(repr(line))

print("--------------------------------")

#Check the timeseries timeline

print(df["CountryCode"].unique())

be_df = df[df["CountryCode"] == "BE"]
print(be_df["DateUTC"].min())
print(be_df["DateUTC"].max())

#Convert datum

be_df["DateUTC"] = pd.to_datetime(
    be_df["DateUTC"]
    ,format="%d-%m-%Y %H:%M"
)

be_df["Hour"] = be_df["DateUTC"].dt.hour
be_df["Month"] = be_df["DateUTC"].dt.month 
be_df["DayOfWeek"] = be_df["DateUTC"].dt.day

print(be_df["DateUTC"].min())

print("--------------------------------")

#First quality control


#Check missing values
print("Missing values \n")
print(be_df.isnull().sum())

#Check duplicates
print("Duplicates\n")
print(be_df.duplicated().sum())


#Test graph

plt.figure(figsize=(15,5))
plt.plot(
    be_df["DateUTC"]
    ,be_df["Value"]
)

plt.title("Belgian Electricity Load")
plt.xlabel("Date")
plt.ylabel("Load")

plt.show()

print("--------------------------------")

#Basic KPI's

print("Basic KPIS\n")

#Mean
print("Mean:\n",be_df["Value"].mean())

#Max load 
print("Max load:\n",be_df["Value"].max())

#Minimum load
print("Min load:\n",be_df["Value"].min())

#Peak
peak =  be_df.loc[be_df["Value"].idxmax()]
print("Peak load is:\n",peak)

#Avg usage per hour
hourly_avg = be_df.groupby("Hour")["Value"].mean()
print("Hourly average is:\n", hourly_avg)

