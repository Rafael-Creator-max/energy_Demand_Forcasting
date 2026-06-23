import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/processed/belgium_load_clean.csv")

df["DateUTC"] = pd.to_datetime(df["DateUTC"])

print("Dataset loaded")
print(df.head())
print(df.shape)

#Test1

print("\nRows per year:")
print(df["Year"].value_counts().sort_index())


#KPI's

print("\n========== KPI ==========")

print("Average Load:", round(df["Value"].mean(), 2))
print("Maximum Load:", round(df["Value"].max(), 2))
print("Minimum Load:", round(df["Value"].min(), 2))

peak = df.loc[df["Value"].idxmax()]

print("\nPeak Moment:")
print(peak)

#AVG ENERGY CONSUMPTION PER HOUR
print("\nAVG hour:")
hourly_avg = df.groupby("Hour")["Value"].mean()
print(hourly_avg)

#Graph
plt.figure(figsize=(10,5))
plt.plot(
    hourly_avg.index,
    hourly_avg.values
)
plt.title("Average Belgian Electricity Load by Hour")
plt.xlabel("Hour")
plt.ylabel("Load (MW)")
plt.grid(True)

plt.savefig("../output/graphs/load_by_hour.png")

#AVG ENERGY CONSUMPTION PER MONTH
monthly_avg = df.groupby("Month")["Value"].mean()

#Graph
plt.figure(figsize=(10,5))
plt.plot(
    monthly_avg.index,
    monthly_avg.values,
    marker="o"
)
plt.title("Average Belgian Electricity Load by Month")
plt.xlabel("Month")
plt.ylabel("Load (MW)")
plt.grid(True)

plt.savefig("../output/graphs/load_by_month.png")