# ==========================================
# PHASE 8.1 : MODEL DEVELOPMENT
# Logistic Regression
# Heart Disease Prediction Project
# ==========================================

# ------------------------------------------
# Step 1 : Import Required Libraries
# ------------------------------------------

from pathlib import Path
import pandas as pd
from sklearn.linear_model import LogisticRegression

# ------------------------------------------
# Step 2 : Project Folder Paths
# ------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "Dataset"

# ------------------------------------------
# Step 3 : Load Training and Testing Data
# ------------------------------------------

X_train = pd.read_csv(DATASET_PATH / "X_train.csv")
X_test = pd.read_csv(DATASET_PATH / "X_test.csv")

y_train = pd.read_csv(DATASET_PATH / "y_train.csv")
y_test = pd.read_csv(DATASET_PATH / "y_test.csv")

print("Dataset Loaded Successfully")

# ------------------------------------------
# Step 4 : Convert Target into 1D Array
# ------------------------------------------

y_train = y_train.values.ravel()
y_test = y_test.values.ravel()

# ------------------------------------------
# Step 5 : Create Logistic Regression Model
# ------------------------------------------

model = LogisticRegression(random_state=42)

print("Model Created Successfully")

# ------------------------------------------
# Step 6 : Train the Model
# ------------------------------------------

model.fit(X_train, y_train)

print("Model Trained Successfully")

# ------------------------------------------
# Step 7 : Predict Testing Data
# ------------------------------------------

y_pred = model.predict(X_test)

print("Prediction Completed")

# ------------------------------------------
# Step 8 : Display First 10 Predictions
# ------------------------------------------

print("\nFirst 10 Predictions")
print(y_pred[:10])

# ------------------------------------------
# Step 9 : Display First 10 Actual Values
# ------------------------------------------

print("\nFirst 10 Actual Values")
print(y_test[:10])

# ------------------------------------------
# Step 10 : Completion Message
# ------------------------------------------

print("\n===================================")
print("Logistic Regression Completed")
print("===================================")