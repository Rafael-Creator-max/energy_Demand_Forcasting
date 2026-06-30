import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load forecast
forecast = pd.read_csv("../data/processed/belgium_load_future_forecast.csv")
forecast["DateUTC"] = pd.to_datetime(forecast["DateUTC"])

# Load real 2026 data
real = pd.read_csv("../data/monthly_hourly_load_values_2026.csv", sep="\t", engine="python")
real["DateUTC"] = pd.to_datetime(
    real["DateUTC"],
    format="%d-%m-%Y %H:%M"
)
# Filter Belgium only
real_be = real[real["CountryCode"] == "BE"].copy()

# Keep only needed columns
real_be = real_be[["DateUTC", "Value"]]
real_be = real_be.rename(columns={"Value": "Actual"})

forecast = forecast.rename(columns={"Forecast": "Prediction"})

# Merge forecast with actual data
comparison = pd.merge(
    forecast,
    real_be,
    on="DateUTC",
    how="inner"
)

print("Comparison data:")
print(comparison.head())
print(comparison.shape)

# Metrics
mae = mean_absolute_error(comparison["Actual"], comparison["Prediction"])
rmse = np.sqrt(mean_squared_error(comparison["Actual"], comparison["Prediction"]))
mape = np.mean(np.abs((comparison["Actual"] - comparison["Prediction"]) / comparison["Actual"])) * 100
r2 = r2_score(comparison["Actual"], comparison["Prediction"])

print("\n========== REAL WORLD VALIDATION ==========")
print("MAE:", round(mae, 2), "MW")
print("RMSE:", round(rmse, 2), "MW")
print("MAPE:", round(mape, 2), "%")
print("R²:", round(r2, 4))

metrics = pd.DataFrame({
    "Metric": [
        "Mean Absolute Error",
        "Root Mean Squared Error",
        "Mean Absolute Percentage Error",
        "R Squared"
    ],
    "Abbreviation": [
        "MAE",
        "RMSE",
        "MAPE",
        "R²"
    ],
    "Value": [
        round(mae, 2),
        round(rmse, 2),
        round(mape, 2),
        round(r2, 4)
    ],
    "Unit": [
        "MW",
        "MW",
        "%",
        ""
    ]
})

metrics.to_csv(
    "../data/processed/model_metrics.csv",
    index=False
)

# Save comparison
comparison.to_csv("../data/processed/belgium_load_real_world_validation.csv", index=False)

# Plot
plt.figure(figsize=(12, 5))
plt.plot(comparison["DateUTC"], comparison["Actual"], label="Actual 2026")
plt.plot(comparison["DateUTC"], comparison["Prediction"], label="Forecast 2026")
plt.title("Real World Validation - Belgium Electricity Load Forecast")
plt.xlabel("Date")
plt.ylabel("Load (MW)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("../reports/real_world_validation_2026.png", dpi=300, bbox_inches="tight")
plt.show()

print("\nReal-world validation saved.")