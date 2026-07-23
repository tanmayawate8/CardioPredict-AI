
# PHASE 10 : BEST MODEL SELECTION
# Heart Disease Prediction Project
# ==========================================

# ------------------------------------------
# Step 1 : Import Required Library
# ------------------------------------------

import pandas as pd

# ------------------------------------------
# Step 2 : Create Model Comparison Table
# Replace these values with your results
# ------------------------------------------

results = {
    "Model": [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "XGBoost"
    ],
    "Accuracy": [0.8641, 0.8424, 0.8967, 0.9185],
    "Precision": [0.8846, 0.8500, 0.9050, 0.9260],
    "Recall": [0.8679, 0.8400, 0.8900, 0.9150],
    "F1 Score": [0.8762, 0.8450, 0.8970, 0.9200]
}

comparison = pd.DataFrame(results)

# ------------------------------------------
# Step 3 : Display Comparison Table
# ------------------------------------------

print("\nModel Comparison\n")
print(comparison)

# ------------------------------------------
# Step 4 : Select Best Model
# ------------------------------------------

best_model = comparison.loc[
    comparison["Accuracy"].idxmax()
]

# ------------------------------------------
# Step 5 : Display Best Model
# ------------------------------------------

print("\n===================================")
print("Best Model Selected")
print("===================================")

print("Model :", best_model["Model"])
print("Accuracy :", best_model["Accuracy"])
print("Precision :", best_model["Precision"])
print("Recall :", best_model["Recall"])
print("F1 Score :", best_model["F1 Score"])

print("\n===================================")
print("Phase 10 Completed Successfully")
print("===================================")