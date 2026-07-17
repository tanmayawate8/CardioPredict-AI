# ==========================================
# PHASE 6 : DATA PREPROCESSING
# Heart Disease Prediction Project
# ==========================================


from pathlib import Path
import pandas as pd
import pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "Dataset"

CURRENT_FOLDER = Path(__file__).resolve().parent

# ------------------------------------------
# Step 3 : Load Cleaned Dataset
# ------------------------------------------

df = pd.read_csv(DATASET_PATH / "cleaned_heart_data.csv")

print("Dataset Loaded Successfully\n")

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
# Step 6 : Separate Features and Target
# ------------------------------------------

X = df.drop("HeartDisease", axis=1)

y = df["HeartDisease"]

print("\nFeatures (X) Shape :", X.shape)
print("Target (y) Shape :", y.shape)

# ------------------------------------------
# Step 7 : Identify Categorical Columns
# ------------------------------------------

categorical_columns = [
    "Sex",
    "ChestPainType",
    "RestingECG",
    "ExerciseAngina",
    "ST_Slope"
]

print("\nCategorical Columns:")
print(categorical_columns)

# ------------------------------------------
# Step 8 : Encode Categorical Columns
# ------------------------------------------

encoders = {}

for column in categorical_columns:

    le = LabelEncoder()

    X[column] = le.fit_transform(X[column])

    encoders[column] = le

print("\nCategorical Columns Encoded Successfully")

# ------------------------------------------
# Step 9 : Save Label Encoders
# ------------------------------------------

with open(CURRENT_FOLDER / "label_encoders.pkl", "wb") as file:

    pickle.dump(encoders, file)

print("Label Encoders Saved Successfully")

# ------------------------------------------
# Step 10 : Display Encoded Dataset
# ------------------------------------------

print("\nEncoded Dataset:")
print(X.head())

# ------------------------------------------
# Step 11 : Display Encoding Mapping
# ------------------------------------------

print("\nEncoding Mapping")

for column in categorical_columns:

    print("\n", column)

    le = encoders[column]

    for original, encoded in zip(le.classes_, range(len(le.classes_))):

        print(original, "-->", encoded)

# ------------------------------------------
# Step 12 : Check Data Types
# ------------------------------------------

print("\nData Types After Encoding:")
print(X.dtypes)

# ------------------------------------------
# Step 13 : Identify Numerical Columns
# ------------------------------------------

numerical_columns = [
    "Age",
    "RestingBP",
    "Cholesterol",
    "FastingBS",
    "MaxHR",
    "Oldpeak"
]

print("\nNumerical Columns:")
print(numerical_columns)

# ------------------------------------------
# Step 14 : Apply Feature Scaling
# ------------------------------------------

scaler = StandardScaler()

X[numerical_columns] = scaler.fit_transform(X[numerical_columns])

print("\nFeature Scaling Completed")

# ------------------------------------------
# Step 15 : Save Scaler
# ------------------------------------------

with open(CURRENT_FOLDER / "scaler.pkl", "wb") as file:

    pickle.dump(scaler, file)

print("Scaler Saved Successfully")

# ------------------------------------------
# Step 16 : Display Scaled Dataset
# ------------------------------------------

print("\nScaled Dataset:")
print(X.head())

# ------------------------------------------
# Step 17 : Combine Features and Target
# ------------------------------------------

preprocessed_df = X.copy()

preprocessed_df["HeartDisease"] = y

# ------------------------------------------
# Step 18 : Display Preprocessed Dataset
# ------------------------------------------

print("\nPreprocessed Dataset:")
print(preprocessed_df.head())

# ------------------------------------------
# Step 19 : Display Dataset Shape
# ------------------------------------------

print("\nPreprocessed Dataset Shape:")
print(preprocessed_df.shape)

# ------------------------------------------
# Step 20 : Check Missing Values
# ------------------------------------------

print("\nMissing Values After Preprocessing:")
print(preprocessed_df.isnull().sum())

# ------------------------------------------
# Step 21 : Display Summary Statistics
# ------------------------------------------

print("\nSummary Statistics:")
print(preprocessed_df.describe())

# ------------------------------------------
# Step 22 : Display Target Distribution
# ------------------------------------------

print("\nTarget Distribution:")
print(preprocessed_df["HeartDisease"].value_counts())

# ------------------------------------------
# Step 23 : Display Feature Names
# ------------------------------------------

print("\nFeature Columns:")
print(list(X.columns))

# ------------------------------------------
# Step 24 : Save Preprocessed Dataset
# ------------------------------------------

preprocessed_df.to_csv(
    DATASET_PATH / "preprocessed_heart_data.csv",
    index=False
)

print("\nPreprocessed Dataset Saved Successfully")


print("\n========================================")
print("Phase 6 Completed Successfully")
print("Files Created Successfully")
print("1. Dataset/preprocessed_heart_data.csv")
print("2. Phase 6 - Data Preprocessing/scaler.pkl")
print("3. Phase 6 - Data Preprocessing/label_encoders.pkl")
print("========================================")