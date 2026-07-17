# ==========================================
# PHASE 7 : TRAIN-TEST SPLITTING
# Heart Disease Prediction Project
# ==========================================

# ------------------------------------------
# Step 1 : Import Required Libraries
# ------------------------------------------

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

# ------------------------------------------
# Step 2 : Project Folder Paths
# ------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "Dataset"

# ------------------------------------------
# Step 3 : Load Preprocessed Dataset
# ------------------------------------------

df = pd.read_csv(DATASET_PATH / "preprocessed_heart_data.csv")

print("Preprocessed Dataset Loaded Successfully\n")

# ------------------------------------------
# Step 4 : Display First 5 Records
# ------------------------------------------

print("First 5 Records:")
print(df.head())

# ------------------------------------------
# Step 5 : Check Dataset Shape
# ------------------------------------------

print("\nDataset Shape:")
print(df.shape)

# ------------------------------------------
# Step 6 : Separate Features (X) and Target (y)
# ------------------------------------------

X = df.drop("HeartDisease", axis=1)
y = df["HeartDisease"]

print("\nFeatures (X) Shape :", X.shape)
print("Target (y) Shape :", y.shape)

# ------------------------------------------
# Step 7 : Split Dataset into Training and Testing
# 80% Training
# 20% Testing
# ------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nDataset Split Completed Successfully")

# ------------------------------------------
# Step 8 : Display Training Dataset Shape
# ------------------------------------------

print("\nTraining Dataset")

print("X_train Shape :", X_train.shape)
print("y_train Shape :", y_train.shape)

# ------------------------------------------
# Step 9 : Display Testing Dataset Shape
# ------------------------------------------

print("\nTesting Dataset")

print("X_test Shape :", X_test.shape)
print("y_test Shape :", y_test.shape)

# ------------------------------------------
# Step 10 : Display First 5 Rows of X_train
# ------------------------------------------

print("\nFirst 5 Rows of X_train")
print(X_train.head())

# ------------------------------------------
# Step 11 : Display First 5 Values of y_train
# ------------------------------------------

print("\nFirst 5 Values of y_train")
print(y_train.head())

# ------------------------------------------
# Step 12 : Display First 5 Rows of X_test
# ------------------------------------------

print("\nFirst 5 Rows of X_test")
print(X_test.head())

# ------------------------------------------
# Step 13 : Display First 5 Values of y_test
# ------------------------------------------

print("\nFirst 5 Values of y_test")
print(y_test.head())

# ------------------------------------------
# Step 14 : Save Training Dataset
# ------------------------------------------

X_train.to_csv(DATASET_PATH / "X_train.csv", index=False)
y_train.to_csv(DATASET_PATH / "y_train.csv", index=False)

# ------------------------------------------
# Step 15 : Save Testing Dataset
# ------------------------------------------

X_test.to_csv(DATASET_PATH / "X_test.csv", index=False)
y_test.to_csv(DATASET_PATH / "y_test.csv", index=False)

# ------------------------------------------
# Step 16 : Completion Message
# ------------------------------------------

print("\n======================================")
print("Phase 7 Completed Successfully")
print("Training and Testing Data Saved")
print("======================================")

print("\nSaved Files:")
print("1. Dataset/X_train.csv")
print("2. Dataset/y_train.csv")
print("3. Dataset/X_test.csv")
print("4. Dataset/y_test.csv")