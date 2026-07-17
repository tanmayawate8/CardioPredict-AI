# ==========================================
# PHASE 4 : DATA CLEANING
# Heart Disease Prediction Project
# ==========================================

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "Dataset"

df = pd.read_csv(DATASET_PATH / "heart.csv")

print("Dataset Loaded Successfully!\n")


print("First 5 Records:")
print(df.head())

print("\nLast 5 Records:")
print(df.tail())

print("\nDataset Shape:")
print(df.shape)

print("\nNumber of Rows :", df.shape[0])
print("Number of Columns :", df.shape[1])

print("\nColumn Names:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)

print("\nDataset Information:")
df.info()

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

df = df.drop_duplicates()

print("\nDataset Shape After Removing Duplicates:")
print(df.shape)

print("\nUnique Values in Sex:")
print(df["Sex"].unique())

print("\nUnique Values in ChestPainType:")
print(df["ChestPainType"].unique())

print("\nUnique Values in RestingECG:")
print(df["RestingECG"].unique())

print("\nUnique Values in ExerciseAngina:")
print(df["ExerciseAngina"].unique())

print("\nUnique Values in ST_Slope:")
print(df["ST_Slope"].unique())

print("\nSummary Statistics:")
print(df.describe())

print("\nMinimum Values:")
print(df.min())

print("\nMaximum Values:")
print(df.max())

print("\nInvalid Age Values:")
print(df[df["Age"] <= 0])

print("\nInvalid RestingBP Values:")
print(df[df["RestingBP"] <= 0])

print("\nInvalid Cholesterol Values:")
print(df[df["Cholesterol"] < 0])

print("\nInvalid MaxHR Values:")
print(df[df["MaxHR"] <= 0])


df.to_csv(DATASET_PATH / "cleaned_heart_data.csv", index=False)


print("\n===================================")
print("Data Cleaning Completed Successfully")
print("Cleaned Dataset Saved Successfully")
print("File Name : cleaned_heart_data.csv")
print("Location : Dataset Folder")
print("===================================")