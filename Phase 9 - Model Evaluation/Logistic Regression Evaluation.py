# ==========================================
# PHASE 9 : MODEL EVALUATION
# Logistic Regression
# Heart Disease Prediction Project
# ==========================================

# ------------------------------------------
# Step 1 : Import Required Libraries
# ------------------------------------------

from pathlib import Path
import pandas as pd

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

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
# Step 4 : Convert Target into 1-D Array
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
# Step 8 : Calculate Accuracy
# ------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy")
print(accuracy)

# ------------------------------------------
# Step 9 : Calculate Precision
# ------------------------------------------

precision = precision_score(y_test, y_pred)

print("\nPrecision")
print(precision)

# ------------------------------------------
# Step 10 : Calculate Recall
# ------------------------------------------

recall = recall_score(y_test, y_pred)

print("\nRecall")
print(recall)

# ------------------------------------------
# Step 11 : Calculate F1 Score
# ------------------------------------------

f1 = f1_score(y_test, y_pred)

print("\nF1 Score")
print(f1)

# ------------------------------------------
# Step 12 : Display Confusion Matrix
# ------------------------------------------

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix")
print(cm)

# ------------------------------------------
# Step 13 : Display Classification Report
# ------------------------------------------

report = classification_report(y_test, y_pred)

print("\nClassification Report")
print(report)

# ------------------------------------------
# Step 14 : Completion Message
# ------------------------------------------

print("\n===================================")
print("Logistic Regression Evaluation Completed")
print("===================================")