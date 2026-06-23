import pandas as pd

df = pd.read_csv("../data/processed/belgium_load_clean.csv")

# Convert datetime
df["DateUTC"] = pd.to_datetime(df["DateUTC"])

# Sort by time
df = df.sort_values("DateUTC")

print("Dataset loaded")
print(df.head())
print(df.shape)

# ==========================
# Time-based features
# ==========================

df["Hour"] = df["DateUTC"].dt.hour
df["DayOfWeek"] = df["DateUTC"].dt.dayofweek
df["Month"] = df["DateUTC"].dt.month
df["Year"] = df["DateUTC"].dt.year

# ==========================
# Lag features
# ==========================

df["Lag_24"] = df["Value"].shift(24)
df["Lag_48"] = df["Value"].shift(48)
df["Lag_168"] = df["Value"].shift(168)

# ==========================
# Rolling features
# ==========================

df["Rolling_24h"] = df["Value"].shift(1).rolling(window=24).mean()
df["Rolling_7d"] = df["Value"].shift(1).rolling(window=168).mean()

# Remove rows with NaN caused by lag/rolling
df = df.dropna()

print("\nFeature engineered dataset:")
print(df.head())
print(df.shape)

# Save processed feature dataset
output_path = "../data/processed/belgium_load_features.csv"
df.to_csv(output_path, index=False)

print(f"\nFeature dataset saved to: {output_path}")