# ==========================================
# PHASE 3 : DATA LOADING
# Heart Disease Prediction Project
# ==========================================

import pandas as pd

df = pd.read_csv("heart.csv")

print("Dataset Loaded Successfully")

# ------------------------------------------
# Step 3 : Display First 5 Records
# ------------------------------------------

print("\nFirst 5 Records:")
print(df.head())

# ------------------------------------------
# Step 4 : Check Dataset Shape
# ------------------------------------------

print("\nDataset Shape:")
print(df.shape)

# ------------------------------------------
# Step 5 : Display Column Names
# ------------------------------------------

print("\nColumn Names:")
print(df.columns)

# ------------------------------------------
# Step 6 : Display Data Types
# ------------------------------------------

print("\nData Types:")
print(df.dtypes)

# ------------------------------------------
# Step 7 : Completion Message
# ------------------------------------------

print("\n===================================")
print("Phase 3 Completed Successfully")
print("===================================")