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

#AVG ENERGY LOAD PER HOUR
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
plt.close()

#AVG ENERGY LOAD PER MONTH
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
plt.close()

print("\nMonthly Average:")
print(monthly_avg)

#WEEKDAY AVG
weekday_avg = df.groupby("DayOfWeek")["Value"].mean()

#Graph
plt.figure(figsize=(10,5))
plt.plot(
    weekday_avg.index,
    weekday_avg.values,
    marker="o"
)
plt.title("Average Belgian Electricity Load by weekday")
plt.xlabel("Weekday")
plt.ylabel("Load (MW)")
plt.grid(True)

plt.savefig("../output/graphs/load_by_weekday.png")
plt.close()

print("\nWeekday Average:")
print(weekday_avg)

#YEAR AVG
yearly_avg = df.groupby("Year")["Value"].mean()

#Graph
plt.figure(figsize=(10,5))
plt.plot(
    yearly_avg.index,
    yearly_avg.values,
    marker="o"
)
plt.title("Average Belgian Electricity Load by year")
plt.xlabel("year")
plt.ylabel("Load (MW)")
plt.grid(True)

plt.savefig("../output/graphs/load_by_year.png")
plt.close()

print("\nYearly Average:")
print(yearly_avg)

#TOP 20 
top_20 = df.nlargest(20,"Value")

#Graph
plt.figure(figsize=(12, 6))
plt.bar(top_20["DateUTC"].astype(str), top_20["Value"])
plt.title("Top 20 Belgian Electricity Load Peaks")
plt.xlabel("Date")
plt.ylabel("Load (MW)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig("../output/graphs/top20_peaks.png")
plt.close()

top_20.to_csv(
    "../output/tables/top20_peaks.csv",
    index=False
)