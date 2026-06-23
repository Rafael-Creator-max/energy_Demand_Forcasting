import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Load predictions
df = pd.read_csv("../data/processed/belgium_load_predictions.csv")
df["DateUTC"] = pd.to_datetime(df["DateUTC"])

# Metrics
mae = mean_absolute_error(df["Value"], df["Prediction"])
rmse = np.sqrt(mean_squared_error(df["Value"], df["Prediction"]))
r2 = r2_score(df["Value"], df["Prediction"])

mape = np.mean(np.abs((df["Value"] - df["Prediction"]) / df["Value"])) * 100

print("========== MODEL EVALUATION ==========")
print("MAE:", round(mae, 2), "MW")
print("RMSE:", round(rmse, 2), "MW")
print("MAPE:", round(mape, 2), "%")
print("R²:", round(r2, 4))

# Plot first 7 days
sample = df.head(24 * 7)

plt.figure(figsize=(12, 5))
plt.plot(sample["DateUTC"], sample["Value"], label="Actual")
plt.plot(sample["DateUTC"], sample["Prediction"], label="Prediction")
plt.title("Actual vs Predicted Electricity Load - First 7 Days")
plt.xlabel("Date")
plt.ylabel("Load (MW)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot full test period
plt.figure(figsize=(12, 5))
plt.plot(df["DateUTC"], df["Value"], label="Actual")
plt.plot(df["DateUTC"], df["Prediction"], label="Prediction")
plt.title("Actual vs Predicted Electricity Load - Full Test Period")
plt.xlabel("Date")
plt.ylabel("Load (MW)")
plt.legend()
plt.tight_layout()
plt.show()

# Error over time
df["Error"] = df["Value"] - df["Prediction"]

plt.figure(figsize=(12, 5))
plt.plot(df["DateUTC"], df["Error"])
plt.title("Forecast Error Over Time")
plt.xlabel("Date")
plt.ylabel("Error (MW)")
plt.tight_layout()
plt.show()

# Save evaluation dataset
df.to_csv("../data/processed/belgium_load_evaluation.csv", index=False)

print("\nEvaluation file saved.")

