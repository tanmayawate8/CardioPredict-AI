# ==========================================
# PHASE 10 : HYPERPARAMETER TUNING
# Heart Disease Prediction Project
# ==========================================

# ------------------------------------------
# Step 1 : Import Required Libraries
# ------------------------------------------

import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from pathlib import Path
import pandas as pd

# ------------------------------------------
# Set Project Path
# ------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "Phase 7 - Train Test Splitting"

# ------------------------------------------
# Load Training Dataset
# ------------------------------------------

X_train = pd.read_csv(DATA_PATH / "X_train.csv")
X_test = pd.read_csv(DATA_PATH / "X_test.csv")

y_train = pd.read_csv(DATA_PATH / "y_train.csv")
y_test = pd.read_csv(DATA_PATH / "y_test.csv")

print("Training and Testing Dataset Loaded Successfully")

# ------------------------------------------
# Step 3 : Convert Target into 1-D Array
# ------------------------------------------

y_train = y_train.values.ravel()

print("Target Converted Successfully")

# ------------------------------------------
# Step 4 : Create Empty List
# (Store Tuning Results)
# ------------------------------------------

results = []

best_model = None
best_model_name = ""
best_accuracy = 0

print("Result Storage Created Successfully")

# ------------------------------------------
# Step 5 : Logistic Regression Parameters
# ------------------------------------------

lr_parameters = [

    {
        "solver": ["liblinear"],
        "penalty": ["l1", "l2"],
        "C": [0.01, 0.1, 1, 10, 100]
    },

    {
        "solver": ["lbfgs"],
        "penalty": ["l2"],
        "C": [0.01, 0.1, 1, 10, 100]
    }

]

print("Logistic Regression Parameters Ready")

# ------------------------------------------
# Step 6 : Decision Tree Parameters
# ------------------------------------------

dt_parameters = {

    "criterion": ["gini", "entropy"],

    "max_depth": [3, 5, 7, 10],

    "min_samples_split": [2, 5, 10]

}

print("Decision Tree Parameters Ready")

# ------------------------------------------
# Step 7 : Random Forest Parameters
# ------------------------------------------

rf_parameters = {

    "n_estimators": [100, 200, 300],

    "max_depth": [5, 10, 15],

    "min_samples_split": [2, 5]

}

print("Random Forest Parameters Ready")

# ------------------------------------------
# Step 8 : XGBoost Parameters
# ------------------------------------------

xgb_parameters = {

    "n_estimators": [100, 200],

    "max_depth": [3, 5, 7],

    "learning_rate": [0.01, 0.1],

    "subsample": [0.8, 1.0]

}

print("XGBoost Parameters Ready")# ------------------------------------------
# Step 9 : Logistic Regression Hyperparameter Tuning
# ------------------------------------------

print("\n========================================")
print("Logistic Regression Hyperparameter Tuning")
print("========================================")

lr_model = LogisticRegression(random_state=42)

lr_grid = GridSearchCV(

    estimator=lr_model,

    param_grid=lr_parameters,

    cv=5,

    scoring="accuracy",

    n_jobs=-1,

    verbose=1

)

lr_grid.fit(X_train, y_train)

print("\nLogistic Regression Tuning Completed")

# ------------------------------------------
# Step 10 : Display Best Parameters
# ------------------------------------------

print("\nBest Parameters")

print(lr_grid.best_params_)

# ------------------------------------------
# Step 11 : Display Best Accuracy
# ------------------------------------------

print("\nBest Cross Validation Accuracy")

print(round(lr_grid.best_score_, 4))

# ------------------------------------------
# Step 12 : Store Logistic Regression Result
# ------------------------------------------

results.append({

    "Model": "Logistic Regression",

    "Best Accuracy": round(lr_grid.best_score_, 4),

    "Best Parameters": str(lr_grid.best_params_)

})

# ------------------------------------------
# Step 13 : Check Best Model
# ------------------------------------------

if lr_grid.best_score_ > best_accuracy:

    best_accuracy = lr_grid.best_score_

    best_model = lr_grid.best_estimator_

    best_model_name = "Logistic Regression"

print("\nCurrent Best Model")
print(best_model_name)

print("Current Best Accuracy")
print(round(best_accuracy, 4))

# ------------------------------------------
# Step 14 : Logistic Regression Summary
# ------------------------------------------

print("\n----------------------------------------")
print("Logistic Regression Summary")
print("----------------------------------------")

print("Model Name : Logistic Regression")

print("Accuracy :", round(lr_grid.best_score_, 4))

print("Parameters :")

print(lr_grid.best_params_)

print("----------------------------------------")

# ------------------------------------------
# End of Logistic Regression Hyperparameter Tuning
# ------------------------------------------

print("\nLogistic Regression Hyperparameter Tuning Finished")
print("\nProceeding to Decision Tree Hyperparameter Tuning...\n")

# ------------------------------------------
# Step 15 : Decision Tree Hyperparameter Tuning
# ------------------------------------------

print("\n========================================")
print("Decision Tree Hyperparameter Tuning")
print("========================================")

dt_model = DecisionTreeClassifier(random_state=42)

dt_grid = GridSearchCV(

    estimator=dt_model,

    param_grid=dt_parameters,

    cv=5,

    scoring="accuracy",

    n_jobs=-1,

    verbose=1

)

dt_grid.fit(X_train, y_train)

print("\nDecision Tree Tuning Completed")

# ------------------------------------------
# Step 16 : Display Best Parameters
# ------------------------------------------

print("\nBest Parameters")

print(dt_grid.best_params_)

# ------------------------------------------
# Step 17 : Display Best Accuracy
# ------------------------------------------

print("\nBest Cross Validation Accuracy")

print(round(dt_grid.best_score_, 4))

# ------------------------------------------
# Step 18 : Store Decision Tree Result
# ------------------------------------------

results.append({

    "Model": "Decision Tree",

    "Best Accuracy": round(dt_grid.best_score_, 4),

    "Best Parameters": str(dt_grid.best_params_)

})

# ------------------------------------------
# Step 19 : Check Best Model
# ------------------------------------------

if dt_grid.best_score_ > best_accuracy:

    best_accuracy = dt_grid.best_score_

    best_model = dt_grid.best_estimator_

    best_model_name = "Decision Tree"

print("\nCurrent Best Model")
print(best_model_name)

print("Current Best Accuracy")
print(round(best_accuracy, 4))

# ------------------------------------------
# Step 20 : Decision Tree Summary
# ------------------------------------------

print("\n----------------------------------------")
print("Decision Tree Summary")
print("----------------------------------------")

print("Model Name : Decision Tree")

print("Accuracy :", round(dt_grid.best_score_, 4))

print("Parameters :")

print(dt_grid.best_params_)

print("----------------------------------------")

# ------------------------------------------
# End of Decision Tree Hyperparameter Tuning
# ------------------------------------------

print("\nDecision Tree Hyperparameter Tuning Finished")
print("\nProceeding to Random Forest Hyperparameter Tuning...\n")

# ------------------------------------------
# Step 21 : Random Forest Hyperparameter Tuning
# ------------------------------------------

print("\n========================================")
print("Random Forest Hyperparameter Tuning")
print("========================================")

rf_model = RandomForestClassifier(random_state=42)

rf_grid = GridSearchCV(

    estimator=rf_model,

    param_grid=rf_parameters,

    cv=5,

    scoring="accuracy",

    n_jobs=-1,

    verbose=1

)

rf_grid.fit(X_train, y_train)

print("\nRandom Forest Tuning Completed")

# ------------------------------------------
# Step 22 : Display Best Parameters
# ------------------------------------------

print("\nBest Parameters")

print(rf_grid.best_params_)

# ------------------------------------------
# Step 23 : Display Best Accuracy
# ------------------------------------------

print("\nBest Cross Validation Accuracy")

print(round(rf_grid.best_score_, 4))

# ------------------------------------------
# Step 24 : Store Random Forest Result
# ------------------------------------------

results.append({

    "Model": "Random Forest",

    "Best Accuracy": round(rf_grid.best_score_, 4),

    "Best Parameters": str(rf_grid.best_params_)

})

# ------------------------------------------
# Step 25 : Check Best Model
# ------------------------------------------

if rf_grid.best_score_ > best_accuracy:

    best_accuracy = rf_grid.best_score_

    best_model = rf_grid.best_estimator_

    best_model_name = "Random Forest"

print("\nCurrent Best Model")
print(best_model_name)

print("Current Best Accuracy")
print(round(best_accuracy, 4))

# ------------------------------------------
# Step 26 : Random Forest Summary
# ------------------------------------------

print("\n----------------------------------------")
print("Random Forest Summary")
print("----------------------------------------")

print("Model Name : Random Forest")

print("Accuracy :", round(rf_grid.best_score_, 4))

print("Parameters :")

print(rf_grid.best_params_)

print("----------------------------------------")

# ------------------------------------------
# End of Random Forest Hyperparameter Tuning
# ------------------------------------------

print("\nRandom Forest Hyperparameter Tuning Finished")
print("\nProceeding to XGBoost Hyperparameter Tuning...\n")

# ------------------------------------------
# Step 27 : XGBoost Hyperparameter Tuning
# ------------------------------------------

print("\n========================================")
print("XGBoost Hyperparameter Tuning")
print("========================================")

xgb_model = XGBClassifier(

    random_state=42,

    eval_metric="logloss"

)

xgb_grid = GridSearchCV(

    estimator=xgb_model,

    param_grid=xgb_parameters,

    cv=5,

    scoring="accuracy",

    n_jobs=-1,

    verbose=1

)

xgb_grid.fit(X_train, y_train)

print("\nXGBoost Tuning Completed")

# ------------------------------------------
# Step 28 : Display Best Parameters
# ------------------------------------------

print("\nBest Parameters")

print(xgb_grid.best_params_)

# ------------------------------------------
# Step 29 : Display Best Accuracy
# ------------------------------------------

print("\nBest Cross Validation Accuracy")

print(round(xgb_grid.best_score_, 4))

# ------------------------------------------
# Step 30 : Store XGBoost Result
# ------------------------------------------

results.append({

    "Model": "XGBoost",

    "Best Accuracy": round(xgb_grid.best_score_, 4),

    "Best Parameters": str(xgb_grid.best_params_)

})

# ------------------------------------------
# Step 31 : Check Best Model
# ------------------------------------------

if xgb_grid.best_score_ > best_accuracy:

    best_accuracy = xgb_grid.best_score_

    best_model = xgb_grid.best_estimator_

    best_model_name = "XGBoost"

print("\nCurrent Best Model")

print(best_model_name)

print("Current Best Accuracy")

print(round(best_accuracy, 4))

# ------------------------------------------
# Step 32 : XGBoost Summary
# ------------------------------------------

print("\n----------------------------------------")
print("XGBoost Summary")
print("----------------------------------------")

print("Model Name : XGBoost")

print("Accuracy :", round(xgb_grid.best_score_, 4))

print("Parameters :")

print(xgb_grid.best_params_)

print("----------------------------------------")

# ------------------------------------------
# Step 33 : Display Best Tuned Model
# ------------------------------------------

print("\n========================================")
print("Best Tuned Model")
print("========================================")

print("Model :", best_model_name)

print("Cross Validation Accuracy :")

print(round(best_accuracy, 4))

# ------------------------------------------
# Step 34 : Create Comparison DataFrame
# ------------------------------------------

comparison_df = pd.DataFrame(results)

print("\n========================================")
print("Hyperparameter Tuning Results")
print("========================================")

print(comparison_df)

# ------------------------------------------
# Step 35 : Sort Models by Accuracy
# ------------------------------------------

comparison_df = comparison_df.sort_values(
    by="Best Accuracy",
    ascending=False
)

print("\nSorted Results")

print(comparison_df)

# ------------------------------------------
# Step 36 : Save Comparison Results
# ------------------------------------------

comparison_df.to_csv(
    "Hyperparameter_Tuning_Results.csv",
    index=False
)

print("\nHyperparameter Tuning Results Saved Successfully")

# ------------------------------------------
# Step 37 : Save Best Tuned Model
# ------------------------------------------

pickle.dump(

    best_model,

    open("heart_disease_model.pkl", "wb")

)

print("Best Tuned Model Saved Successfully")

# ------------------------------------------
# Step 38 : Display Best Model Information
# ------------------------------------------

print("\n========================================")
print("Final Best Tuned Model")
print("========================================")

print("Model Name :")
print(best_model_name)

print("\nBest Cross Validation Accuracy :")
print(round(best_accuracy, 4))

print("\nBest Parameters :")

if best_model_name == "Logistic Regression":
    print(lr_grid.best_params_)

elif best_model_name == "Decision Tree":
    print(dt_grid.best_params_)

elif best_model_name == "Random Forest":
    print(rf_grid.best_params_)

elif best_model_name == "XGBoost":
    print(xgb_grid.best_params_)

# ------------------------------------------
# Step 39 : Display Generated Files
# ------------------------------------------

print("\nGenerated Files")

print("1. Hyperparameter_Tuning_Results.csv")

print("2. heart_disease_model.pkl")

# ------------------------------------------
# Step 40 : Completion Message
# ------------------------------------------

print("\n========================================")
print("PHASE 10 COMPLETED SUCCESSFULLY")
print("Hyperparameter Tuning Completed")
print("========================================")

print("\nBest Tuned Model Selected Successfully")

print("Project Ready For")

print("Phase 11 : Model Serialization / Deployment")