import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

#Load feature dataset
df = pd.read_csv("../data/processed/belgium_load_features.csv")
df["DateUTC"] = pd.to_datetime(df["DateUTC"])

#Features and target
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

#Time-based train/test split
split_date = "2024-01-01"

train = df[df["DateUTC"] < split_date]
test = df[df["DateUTC"] >= split_date].copy()

X_train = train[features]
y_train = train[target]

X_test = test[features]
y_test = test[target]

#Model
model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)

#Predictions
test["Prediction"] = model.predict(X_test)

#Evaluation
mae = mean_absolute_error(y_test, test["Prediction"])
rmse = np.sqrt(mean_squared_error(y_test, test["Prediction"]))

print("Model results")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))

print(test[["DateUTC", "Value", "Prediction"]].head())

test.to_csv("../data/processed/belgium_load_predictions.csv", index=False)

print("Predictions saved.")

#Features 
#----------------
importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print(importance)

plt.figure(figsize=(8,5))
plt.barh(
    importance["Feature"],
    importance["Importance"]
)

plt.title("Feature Importance")
plt.tight_layout()
plt.savefig(
    "../reports/feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)

importance.to_csv(
    "../data/processed/feature_importance.csv",
    index=False
)

plt.show()
plt.close()

