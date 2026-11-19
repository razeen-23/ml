
import pandas as pd
import numpy as np
from io import StringIO

# ==========================================
# 1. LOAD DATASET
# ==========================================

data = """House ID,Sqft,Bedrooms,bathrooms,Floors,Year Built,Lot Size (sqft),garage_spaces,Has_Pool,Neighborhood,CONDITION,dist_to_center,Price,notes
590,1426,1,1,2,2018,nan,2,0,Downtown,Good,2.7,326200,
489,1826,3,2,1,1976,5948,1,0,rural,Good,-5.0,183900,
754,2581,4,3,1,1965,10121,1,0,Suburb,Fair,nan,393200,
995,1484,2,2,1,1975,4205,3,0,UPTOWN,Fair,1.9,285300,
885,2050,N/A,2,2,1984,4174,2,0,Downtown,Poor,2.8,318200,
758,2633,3,2,2,1961,8453,2,0,Uptown,N/A,5.4,411900,
52,1681,3,2,2,2008,4209,2,0,Downtown,Good,9.7,384200,
416,1694,1,2,2,2017,7022,2,0,Suburb,Excellent,15.1,330500,
830,1687,three,1,1,1959,3337,1,0,Suburb,Good,15.2,217100,
62,1897,3,2,2,2006,7106,0,0,Suburb,Fair,11.3,N/A,
28,1829,3,2,1,2022,5877,2,0,Downtown,Good,1.2,380100,
643,1651,1,1,1,2016,3551,3,0,Down town,Gud,2.9,348400,
993,1519,4,2,1,1991,2696,1,0,Lakeside,Good,21.2,365800,
355,1536,3,2,2,2002,5500,2,0,Suburb,Excellent,17.2,337900,
996,1724,3,2,2,1999,7739,1,0,nan,Good,14.5,"277,200",
"""

df = pd.read_csv(StringIO(data), na_values=["nan", "N/A", ""])

print("Original Dataset:")
print(df.head())


# ==========================================
# 2. REMOVE DUPLICATE RECORDS
# ==========================================

df.drop_duplicates(subset=["House ID"], keep="first", inplace=True)


# ==========================================
# 3. CLEAN COLUMN NAMES
# ==========================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# ==========================================
# 4. CLEAN NUMERIC COLUMNS
# ==========================================

# Convert price by removing commas
df["price"] = (
    df["price"]
    .astype("string")
    .str.replace(",", "", regex=False)
)

# Correct word-based bedroom value
df["bedrooms"] = (
    df["bedrooms"]
    .replace({
        "three": "3",
        "Three": "3"
    })
)

# Convert numeric columns
numeric_columns = [
    "house_id",
    "sqft",
    "bedrooms",
    "bathrooms",
    "floors",
    "year_built",
    "lot_size_(sqft)",
    "garage_spaces",
    "has_pool",
    "dist_to_center",
    "price"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# ==========================================
# 5. CLEAN NEIGHBORHOOD COLUMN
# ==========================================

df["neighborhood"] = (
    df["neighborhood"]
    .astype("string")
    .str.strip()
    .str.lower()
)

neighborhood_mapping = {
    "downtown": "Downtown",
    "down town": "Downtown",
    "uptown": "Uptown",
    "suburb": "Suburb",
    "rural": "Rural",
    "lakeside": "Lakeside"
}

df["neighborhood"] = (
    df["neighborhood"]
    .map(neighborhood_mapping)
)


# ==========================================
# 6. CLEAN CONDITION COLUMN
# ==========================================

df["condition"] = (
    df["condition"]
    .astype("string")
    .str.strip()
    .str.lower()
)

condition_mapping = {
    "good": "Good",
    "gud": "Good",
    "fair": "Fair",
    "poor": "Poor",
    "excellent": "Excellent"
}

df["condition"] = df["condition"].map(condition_mapping)


# ==========================================
# 7. HANDLE MISSING VALUES
# ==========================================

# Fill numerical missing values with median
numeric_fill_columns = [
    "bedrooms",
    "bathrooms",
    "floors",
    "year_built",
    "lot_size_(sqft)",
    "garage_spaces",
    "dist_to_center",
    "price"
]

for col in numeric_fill_columns:
    df[col] = df[col].fillna(df[col].median())


# Fill categorical missing values with mode
categorical_columns = [
    "neighborhood",
    "condition"
]

for col in categorical_columns:
    if df[col].notna().any():
        df[col] = df[col].fillna(df[col].mode()[0])


# ==========================================
# 8. CORRECT INVALID VALUES
# ==========================================

# Distance cannot be negative
df.loc[df["dist_to_center"] < 0, "dist_to_center"] = np.nan

# Replace invalid distance with median
df["dist_to_center"] = df["dist_to_center"].fillna(
    df["dist_to_center"].median()
)

# Ensure pool values are binary
df["has_pool"] = df["has_pool"].where(
    df["has_pool"].isin([0, 1]), np.nan
)

df["has_pool"] = df["has_pool"].fillna(
    df["has_pool"].mode()[0]
)


# ==========================================
# 9. CONVERT DATA TYPES
# ==========================================

integer_columns = [
    "house_id",
    "sqft",
    "bedrooms",
    "bathrooms",
    "floors",
    "year_built",
    "lot_size_(sqft)",
    "garage_spaces",
    "has_pool",
    "price"
]

for col in integer_columns:
    df[col] = df[col].round().astype("int64")


# ==========================================
# 10. HANDLE NOTES COLUMN
# ==========================================

df["notes"] = df["notes"].fillna("No notes")

df["notes"] = df["notes"].astype(str).str.strip()


# ==========================================
# 11. RESET INDEX
# ==========================================

df.reset_index(drop=True, inplace=True)


# ==========================================
# 12. CHECK CLEANED DATASET
# ==========================================

print("\nCleaned Dataset:")
print(df)

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated(subset=["house_id"]).sum())


# ==========================================
# 13. SAVE CLEANED DATASET
# ==========================================

df.to_csv("cleaned_housing_dataset1.csv", index=False)

print("\nCleaned dataset saved successfully!")
