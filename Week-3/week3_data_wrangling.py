# ==============================================================================
# WEEK 3: PYTHON & DATA WRANGLING PROJECT
# Tasks: Clean messy data, handle nulls, filter rows, create columns, visualize
# ==============================================================================

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set visual style
sns.set_theme(style="whitegrid")

# ------------------------------------------------------------------------------
# 1. LOAD DATASET & INITIAL INSPECTION
# ------------------------------------------------------------------------------
# Read CSV (use sep=r'\s+' if your raw file is tab/space separated)
try:
    df = pd.read_csv("dirty_data.csv")
except Exception:
    df = pd.read_csv("dirty_data.csv", sep=r"\s+")

print("=" * 65)
print("1. RAW DATA OVERVIEW")
print("=" * 65)
print(df.head(10))

print("\nMissing values before cleaning:")
print(df.isnull().sum())
print(f"Duplicates before cleaning: {df.duplicated().sum()}")


# ------------------------------------------------------------------------------
# 2. DATA CLEANING & HANDLING MISSING VALUES
# ------------------------------------------------------------------------------

# Step A: Remove duplicate rows (Removes the duplicate Dec 12 row)
df = df.drop_duplicates().reset_index(drop=True)

# Step B: Clean and Standardize the 'Date' column
# Clean out stray quotes: "2020/12/01'" -> "2020/12/01"
df["Date"] = df["Date"].astype(str).str.replace("'", "").str.strip()

# Convert to standard Datetime format (handles '20201226' and bad formats)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce", format="mixed")

# Drop rows with missing Date (one row has no date)
df = df.dropna(subset=["Date"]).reset_index(drop=True)

# Step C: Fix Duration typo / outlier (450 mins is a typo for 45 mins)
df.loc[df["Duration"] > 120, "Duration"] = 45

# Step D: Fill missing values in Calories with the column Median
median_calories = round(df["Calories"].median(), 1)
df["Calories"] = df["Calories"].fillna(median_calories)

# Step E: Fix Logical Error (Pulse cannot be greater than Maxpulse)
# If Pulse > Maxpulse, swap their values
mask = df["Pulse"] > df["Maxpulse"]
df.loc[mask, ["Pulse", "Maxpulse"]] = df.loc[
    mask, ["Maxpulse", "Pulse"]
].values

print("\n" + "=" * 65)
print("2. CLEANED DATA CHECK (MISSING VALUES REMOVED)")
print("=" * 65)
print(df.isnull().sum())


# ------------------------------------------------------------------------------
# 3. FEATURE ENGINEERING: CREATE NEW COLUMNS (REQUIREMENT)
# ------------------------------------------------------------------------------

# New Column 1: Calories burned per minute
df["Calories_per_Min"] = (df["Calories"] / df["Duration"]).round(2)

# New Column 2: Heart Rate Reserve / Pulse Range
df["Pulse_Difference"] = df["Maxpulse"] - df["Pulse"]

# New Column 3: Workout Intensity Category (CASE / Categorization)
df["Workout_Intensity"] = np.where(
    df["Pulse"] >= 105,
    "High Intensity",
    np.where(df["Pulse"] >= 98, "Moderate Intensity", "Low Intensity"),
)

# New Column 4: Day of Week from Date
df["Day_Name"] = df["Date"].dt.day_name()

print("\n" + "=" * 65)
print("3. SAMPLE DATA WITH NEW COLUMNS CREATED")
print("=" * 65)
print(
    df[
        [
            "Date",
            "Duration",
            "Pulse",
            "Calories",
            "Calories_per_Min",
            "Workout_Intensity",
        ]
    ].head(8)
)


# ------------------------------------------------------------------------------
# 4. ROW FILTERING (REQUIREMENT)
# ------------------------------------------------------------------------------
print("\n" + "=" * 65)
print("4. FILTERED DATASETS")
print("=" * 65)

# Filter 1: Workouts burning more than 300 Calories
high_calorie_workouts = df[df["Calories"] >= 300]
print(
    f"Number of workouts burning >= 300 calories: {len(high_calorie_workouts)}"
)

# Filter 2: High-Intensity Workouts with Duration of 60 mins
intense_60min = df[
    (df["Workout_Intensity"] == "High Intensity") & (df["Duration"] == 60)
]
print(
    f"Number of 60-min High Intensity workouts: {len(intense_60min)}\nFirst 3 rows:"
)
print(
    intense_60min[
        ["Date", "Duration", "Pulse", "Calories", "Workout_Intensity"]
    ].head(3)
)


# ------------------------------------------------------------------------------
# 5. DATA VISUALIZATION (MATPLOTLIB & SEABORN)
# ------------------------------------------------------------------------------

# Chart 1: Calories Burned vs Duration by Intensity
plt.figure(figsize=(9, 5))
sns.scatterplot(
    data=df,
    x="Duration",
    y="Calories",
    hue="Workout_Intensity",
    palette="Set2",
    s=120,
)
plt.title("Calories Burned vs Duration by Intensity", fontsize=14, weight="bold")
plt.xlabel("Duration (Minutes)")
plt.ylabel("Calories Burned")
plt.tight_layout()
plt.savefig("calories_vs_duration.png")
plt.show()

# Chart 2: Correlation Heatmap
plt.figure(figsize=(8, 5))
numeric_df = df[
    [
        "Duration",
        "Pulse",
        "Maxpulse",
        "Calories",
        "Calories_per_Min",
        "Pulse_Difference",
    ]
]
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Health Metrics Correlation Heatmap", fontsize=14, weight="bold")
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
plt.show()

# ------------------------------------------------------------------------------
# 6. EXPORT CLEANED DATASET
# ------------------------------------------------------------------------------
df.to_csv("cleaned_workout_data.csv", index=False)
print("\nCleaned file exported successfully as: 'cleaned_workout_data.csv'")