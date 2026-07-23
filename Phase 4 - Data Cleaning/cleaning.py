# ==========================================
# PHASE 4 : DATA CLEANING
# Heart Disease Prediction Project
# ==========================================

import pandas as pd
from pathlib import Path


# ==========================================
# STEP 1 : SET PROJECT PATHS
# ==========================================

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset folder
DATASET_PATH = BASE_DIR / "Dataset"

# Input dataset
INPUT_FILE = DATASET_PATH / "heart.csv"

# Output cleaned dataset
OUTPUT_FILE = DATASET_PATH / "cleaned_heart_data.csv"


# ==========================================
# STEP 2 : LOAD DATASET
# ==========================================

print("\n==========================================")
print("PHASE 4 : DATA CLEANING")
print("Heart Disease Prediction Project")
print("==========================================")

print("\nLoading Dataset...")

try:
    df = pd.read_csv(INPUT_FILE)
    print("Dataset Loaded Successfully!")

except FileNotFoundError:
    print("\nERROR: Dataset file not found!")
    print(f"Expected Location: {INPUT_FILE}")
    exit()


# ==========================================
# STEP 3 : DISPLAY ORIGINAL DATASET
# ==========================================

print("\n==========================================")
print("ORIGINAL DATASET INFORMATION")
print("==========================================")

print("\nFirst 5 Records:")
print(df.head())

print("\nLast 5 Records:")
print(df.tail())

print("\nDataset Shape:")
print(df.shape)

print("\nNumber of Rows:", df.shape[0])
print("Number of Columns:", df.shape[1])

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)


# ==========================================
# STEP 4 : CHECK REQUIRED COLUMNS
# ==========================================

required_columns = [
    "Age",
    "Sex",
    "ChestPainType",
    "RestingBP",
    "Cholesterol",
    "FastingBS",
    "RestingECG",
    "MaxHR",
    "ExerciseAngina",
    "Oldpeak",
    "ST_Slope",
    "HeartDisease"
]

print("\n==========================================")
print("CHECKING REQUIRED COLUMNS")
print("==========================================")

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print("ERROR: Required columns are missing:")
    print(missing_columns)

    print("\nExpected Columns:")
    print(required_columns)

    exit()

else:

    print("All required columns are present.")


# ==========================================
# STEP 5 : DATASET INFORMATION
# ==========================================

print("\n==========================================")
print("DATASET INFORMATION")
print("==========================================")

df.info()


# ==========================================
# STEP 6 : CHECK MISSING VALUES
# ==========================================

print("\n==========================================")
print("MISSING VALUE CHECK")
print("==========================================")

missing_values = df.isnull().sum()

print(missing_values)

total_missing = missing_values.sum()

if total_missing == 0:

    print("\nNo missing values found.")

else:

    print(
        f"\nTotal Missing Values Found: {total_missing}"
    )

    # Remove rows containing missing values
    df = df.dropna()

    print(
        "Rows containing missing values have been removed."
    )


# ==========================================
# STEP 7 : CHECK DUPLICATE RECORDS
# ==========================================

print("\n==========================================")
print("DUPLICATE RECORD CHECK")
print("==========================================")

duplicate_count = df.duplicated().sum()

print(
    "Duplicate Records Found:",
    duplicate_count
)

if duplicate_count > 0:

    df = df.drop_duplicates()

    print(
        "Duplicate records removed successfully."
    )

else:

    print(
        "No duplicate records found."
    )


# ==========================================
# STEP 8 : CHECK CATEGORICAL VALUES
# ==========================================

print("\n==========================================")
print("CATEGORICAL VALUE CHECK")
print("==========================================")


# Sex
print("\nSex Values:")
print(df["Sex"].unique())


# Chest Pain Type
print("\nChest Pain Type Values:")
print(df["ChestPainType"].unique())


# Resting ECG
print("\nResting ECG Values:")
print(df["RestingECG"].unique())


# Exercise Induced Angina
print("\nExercise Angina Values:")
print(df["ExerciseAngina"].unique())


# ST Slope
print("\nST Slope Values:")
print(df["ST_Slope"].unique())


# ==========================================
# STEP 9 : VALIDATE CATEGORICAL VALUES
# ==========================================

print("\n==========================================")
print("VALIDATING CATEGORICAL VALUES")
print("==========================================")


valid_sex = ["M", "F"]

valid_chest_pain = [
    "ATA",
    "NAP",
    "ASY",
    "TA"
]

valid_resting_ecg = [
    "Normal",
    "ST",
    "LVH"
]

valid_exercise_angina = [
    "Y",
    "N"
]

valid_st_slope = [
    "Up",
    "Flat",
    "Down"
]


# Check invalid Sex values
invalid_sex = df[
    ~df["Sex"].isin(valid_sex)
]

print(
    "\nInvalid Sex Records:",
    len(invalid_sex)
)


# Check invalid ChestPainType values
invalid_chest_pain = df[
    ~df["ChestPainType"].isin(valid_chest_pain)
]

print(
    "Invalid Chest Pain Records:",
    len(invalid_chest_pain)
)


# Check invalid RestingECG values
invalid_ecg = df[
    ~df["RestingECG"].isin(valid_resting_ecg)
]

print(
    "Invalid Resting ECG Records:",
    len(invalid_ecg)
)


# Check invalid ExerciseAngina values
invalid_angina = df[
    ~df["ExerciseAngina"].isin(valid_exercise_angina)
]

print(
    "Invalid Exercise Angina Records:",
    len(invalid_angina)
)


# Check invalid ST_Slope values
invalid_slope = df[
    ~df["ST_Slope"].isin(valid_st_slope)
]

print(
    "Invalid ST Slope Records:",
    len(invalid_slope)
)


# ==========================================
# STEP 10 : VALIDATE NUMERICAL VALUES
# ==========================================

print("\n==========================================")
print("NUMERICAL VALUE VALIDATION")
print("==========================================")


# Age
invalid_age = df[
    (df["Age"] <= 0) |
    (df["Age"] > 120)
]

print(
    "\nInvalid Age Records:",
    len(invalid_age)
)


# Resting Blood Pressure
invalid_bp = df[
    (df["RestingBP"] <= 0)
]

print(
    "Invalid Resting BP Records:",
    len(invalid_bp)
)


# Cholesterol
invalid_cholesterol = df[
    (df["Cholesterol"] < 0)
]

print(
    "Invalid Cholesterol Records:",
    len(invalid_cholesterol)
)


# Maximum Heart Rate
invalid_max_hr = df[
    (df["MaxHR"] <= 0)
]

print(
    "Invalid MaxHR Records:",
    len(invalid_max_hr)
)


# Oldpeak
invalid_oldpeak = df[
    df["Oldpeak"] < 0
]

print(
    "Invalid Oldpeak Records:",
    len(invalid_oldpeak)
)


# ==========================================
# STEP 11 : VALIDATE TARGET VARIABLE
# ==========================================

print("\n==========================================")
print("TARGET VARIABLE CHECK")
print("==========================================")

print("\nTarget Column: HeartDisease")

print("\nUnique Target Values:")
print(
    sorted(
        df["HeartDisease"].unique()
    )
)

print("\nTarget Distribution:")
print(
    df["HeartDisease"].value_counts()
)


# Check target values
valid_target_values = [0, 1]

invalid_target = df[
    ~df["HeartDisease"].isin(
        valid_target_values
    )
]

print(
    "\nInvalid Target Records:",
    len(invalid_target)
)


print("\nTarget Mapping:")
print(
    "0 = No Heart Disease"
)

print(
    "1 = Heart Disease"
)


# ==========================================
# STEP 12 : REMOVE INVALID RECORDS
# ==========================================

print("\n==========================================")
print("REMOVING INVALID RECORDS")
print("==========================================")


original_rows = len(df)


# Remove invalid numerical records
df = df[
    (df["Age"] > 0) &
    (df["Age"] <= 120) &
    (df["RestingBP"] > 0) &
    (df["Cholesterol"] >= 0) &
    (df["MaxHR"] > 0) &
    (df["Oldpeak"] >= 0)
]


# Remove invalid categorical records
df = df[
    df["Sex"].isin(valid_sex) &
    df["ChestPainType"].isin(valid_chest_pain) &
    df["RestingECG"].isin(valid_resting_ecg) &
    df["ExerciseAngina"].isin(valid_exercise_angina) &
    df["ST_Slope"].isin(valid_st_slope)
]


# Remove invalid target records
df = df[
    df["HeartDisease"].isin(
        valid_target_values
    )
]


removed_rows = (
    original_rows - len(df)
)


print(
    "Invalid Records Removed:",
    removed_rows
)


# ==========================================
# STEP 13 : FINAL DUPLICATE CHECK
# ==========================================

print("\n==========================================")
print("FINAL DUPLICATE CHECK")
print("==========================================")

final_duplicates = df.duplicated().sum()

print(
    "Remaining Duplicate Records:",
    final_duplicates
)


if final_duplicates > 0:

    df = df.drop_duplicates()

    print(
        "Remaining duplicates removed."
    )

else:

    print(
        "No duplicate records remaining."
    )


# ==========================================
# STEP 14 : FINAL MISSING VALUE CHECK
# ==========================================

print("\n==========================================")
print("FINAL MISSING VALUE CHECK")
print("==========================================")

final_missing = df.isnull().sum()

print(final_missing)

if final_missing.sum() == 0:

    print(
        "\nNo missing values remaining."
    )

else:

    print(
        "\nWARNING: Missing values still exist."
    )


# ==========================================
# STEP 15 : FINAL DATASET SUMMARY
# ==========================================

print("\n==========================================")
print("FINAL CLEANED DATASET SUMMARY")
print("==========================================")

print(
    "\nFinal Dataset Shape:",
    df.shape
)

print(
    "\nFinal Number of Rows:",
    len(df)
)

print(
    "Final Number of Columns:",
    len(df.columns)
)

print(
    "\nFinal Column Names:"
)

print(
    df.columns.tolist()
)


# ==========================================
# STEP 16 : FINAL TARGET DISTRIBUTION
# ==========================================

print("\n==========================================")
print("FINAL TARGET DISTRIBUTION")
print("==========================================")

print(
    df["HeartDisease"].value_counts()
)

print(
    "\n0 = No Heart Disease"
)

print(
    "1 = Heart Disease"
)


# ==========================================
# STEP 17 : SAVE CLEANED DATASET
# ==========================================

print("\n==========================================")
print("SAVING CLEANED DATASET")
print("==========================================")

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "\nCleaned Dataset Saved Successfully!"
)

print(
    "File Name:",
    OUTPUT_FILE.name
)

print(
    "Location:",
    OUTPUT_FILE
)


# ==========================================
# STEP 18 : FINAL VERIFICATION
# ==========================================

print("\n==========================================")
print("FINAL VERIFICATION")
print("==========================================")

print(
    "\nMissing Values:",
    df.isnull().sum().sum()
)

print(
    "Duplicate Records:",
    df.duplicated().sum()
)

print(
    "Target Values:",
    sorted(
        df["HeartDisease"].unique()
    )
)

print(
    "Final Dataset Shape:",
    df.shape
)


# ==========================================
# COMPLETION MESSAGE
# ==========================================

print("\n==========================================")
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("==========================================")

print(
    "\nNext Phase:"
)

print(
    "Proceed to Data Preprocessing."
)

print(
    "\nImportant:"
)

print(
    "Do NOT perform Label Encoding or "
    "Standard Scaling in this Data Cleaning phase."
)

print(
    "Perform Encoding and Scaling in "
    "the Data Preprocessing phase."
)

print(
    "\n==========================================")