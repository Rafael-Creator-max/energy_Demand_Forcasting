import pandas as pd
from xgboost import XGBRegressor
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("../data/processed/belgium_load_features.csv")
df["DateUTC"] = pd.to_datetime(df["DateUTC"])
df = df.sort_values("DateUTC")

features = [
    "Hour",
    "DayOfWeek",
    "Month",
    "Year",
    "Lag_24",
    "Lag_48",
    "Lag_168",
    "Rolling_24h",
    "Rolling_7d"
]

target = "Value"

X = df[features]
y = df[target]

# Train model on all available data
model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    random_state=42
)

model.fit(X, y)

# Forecast settings
forecast_hours = 24 * 30

history = df[["DateUTC", "Value"]].copy()
future_predictions = []

last_date = history["DateUTC"].max()

for i in range(1, forecast_hours + 1):
    next_date = last_date + pd.Timedelta(hours=i)

    temp = history.copy()

    lag_24 = temp["Value"].iloc[-24]
    lag_48 = temp["Value"].iloc[-48]
    lag_168 = temp["Value"].iloc[-168]

    rolling_24h = temp["Value"].iloc[-24:].mean()
    rolling_7d = temp["Value"].iloc[-168:].mean()

    row = pd.DataFrame([{
        "Hour": next_date.hour,
        "DayOfWeek": next_date.dayofweek,
        "Month": next_date.month,
        "Year": next_date.year,
        "Lag_24": lag_24,
        "Lag_48": lag_48,
        "Lag_168": lag_168,
        "Rolling_24h": rolling_24h,
        "Rolling_7d": rolling_7d
    }])

    prediction = model.predict(row)[0]

    future_predictions.append({
        "DateUTC": next_date,
        "Forecast": prediction
    })

    history = pd.concat([
        history,
        pd.DataFrame([{
            "DateUTC": next_date,
            "Value": prediction
        }])
    ], ignore_index=True)

future_df = pd.DataFrame(future_predictions)

print(future_df.head())
print(future_df.tail())

future_df.to_csv("../data/processed/belgium_load_future_forecast.csv", index=False)

# Plot forecast
plt.figure(figsize=(12, 5))
plt.plot(future_df["DateUTC"], future_df["Forecast"])
plt.title("Belgium Electricity Load Forecast - Next 30 Days")
plt.xlabel("Date")
plt.ylabel("Forecast Load (MW)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("../reports/future_forecast_30_days.png", dpi=300, bbox_inches="tight")
plt.show()

print("Future forecast saved.")