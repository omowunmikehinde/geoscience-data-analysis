"""
Geological and Geophysical Data Analysis

Independent portfolio project using a synthetic geoscience dataset.
The workflow demonstrates basic data quality control, descriptive
statistics, correlation analysis, and visualization.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# Define project paths
ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "geoscience_sample.csv"
FIGURES_DIR = ROOT / "figures"

FIGURES_DIR.mkdir(exist_ok=True)


# Load dataset
df = pd.read_csv(DATA_FILE)

print("=" * 60)
print("GEOLOGICAL AND GEOPHYSICAL DATA ANALYSIS")
print("=" * 60)

print(f"\nDataset dimensions: {df.shape[0]} rows × {df.shape[1]} columns")


# ---------------------------------------------------------
# 1. Data Quality Control
# ---------------------------------------------------------

print("\n1. DATA QUALITY CHECK")
print("-" * 40)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate records:", df.duplicated().sum())

print("\nData types:")
print(df.dtypes)


# ---------------------------------------------------------
# 2. Descriptive Statistics
# ---------------------------------------------------------

print("\n2. DESCRIPTIVE STATISTICS")
print("-" * 40)

numeric_columns = [
    "elevation_m",
    "magnetic_intensity_nT",
    "potassium_percent",
    "uranium_ppm",
    "thorium_ppm",
]

statistics = df[numeric_columns].describe()

print(statistics.round(2))


# ---------------------------------------------------------
# 3. Geological Unit Summary
# ---------------------------------------------------------

print("\n3. DATA BY GEOLOGICAL UNIT")
print("-" * 40)

unit_summary = (
    df.groupby("geological_unit")[numeric_columns]
    .mean()
    .round(2)
)

print(unit_summary)


# ---------------------------------------------------------
# 4. Correlation Analysis
# ---------------------------------------------------------

print("\n4. CORRELATION MATRIX")
print("-" * 40)

correlation = df[numeric_columns].corr().round(2)

print(correlation)


# Create correlation plot
fig, ax = plt.subplots(figsize=(8, 6))

image = ax.imshow(correlation, aspect="auto")

ax.set_xticks(
    range(len(numeric_columns)),
    numeric_columns,
    rotation=45,
    ha="right",
)

ax.set_yticks(
    range(len(numeric_columns)),
    numeric_columns,
)

ax.set_title("Correlation Matrix of Geoscience Variables")

fig.colorbar(
    image,
    ax=ax,
    label="Correlation coefficient",
)

fig.tight_layout()

fig.savefig(
    FIGURES_DIR / "correlation_matrix.png",
    dpi=200,
)

plt.close(fig)


# ---------------------------------------------------------
# 5. Magnetic Intensity by Geological Unit
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 5))

units = [
    "Granite",
    "Gneiss",
    "Schist",
    "Pegmatite",
]

magnetic_data = [
    df.loc[
        df["geological_unit"] == unit,
        "magnetic_intensity_nT",
    ].dropna()
    for unit in units
]

ax.boxplot(
    magnetic_data,
    labels=units,
)

ax.set_xlabel("Geological unit")
ax.set_ylabel("Magnetic intensity (nT)")
ax.set_title("Magnetic Intensity by Geological Unit")

fig.tight_layout()

fig.savefig(
    FIGURES_DIR / "magnetic_by_geological_unit.png",
    dpi=200,
)

plt.close(fig)


# ---------------------------------------------------------
# 6. Potassium–Thorium Relationship
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(7, 5))

for unit in units:

    subset = df[
        df["geological_unit"] == unit
    ].dropna(
        subset=[
            "potassium_percent",
            "thorium_ppm",
        ]
    )

    ax.scatter(
        subset["potassium_percent"],
        subset["thorium_ppm"],
        label=unit,
        alpha=0.7,
    )

ax.set_xlabel("Potassium (%)")
ax.set_ylabel("Thorium (ppm)")
ax.set_title("Potassium–Thorium Relationship")
ax.legend()

fig.tight_layout()

fig.savefig(
    FIGURES_DIR / "potassium_thorium.png",
    dpi=200,
)

plt.close(fig)


print("\n" + "=" * 60)
print("Analysis complete.")
print(f"Figures saved to: {FIGURES_DIR}")
print("=" * 60)
