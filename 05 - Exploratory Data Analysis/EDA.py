# ==========================================================
# PHASE 5 : EXPLORATORY DATA ANALYSIS (EDA)
# Heart Disease Prediction Project
# ========================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.preprocessing import LabelEncoder

# ----------------------------------------------------------
# Step 2 : Load Dataset
# ----------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "Dataset"

df = pd.read_csv(DATASET_PATH / "cleaned_heart_data.csv")

print("=" * 60)
print("PHASE 5 : EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print("\nDataset Loaded Successfully.")

# ----------------------------------------------------------
# Step 3 : Display First 5 Records
# ----------------------------------------------------------

print("\nFirst 5 Records")
print(df.head())

# ----------------------------------------------------------
# Step 4 : Display Last 5 Records
# ----------------------------------------------------------

print("\nLast 5 Records")
print(df.tail())

# ----------------------------------------------------------
# Step 5 : Dataset Shape
# ----------------------------------------------------------

print("\nDataset Shape")
print(df.shape)

# ----------------------------------------------------------
# Step 6 : Dataset Information
# ----------------------------------------------------------

print("\nDataset Information")
df.info()

# ----------------------------------------------------------
# Step 7 : Data Types
# ----------------------------------------------------------

print("\nData Types")
print(df.dtypes)

# ----------------------------------------------------------
# Step 8 : Summary Statistics
# ----------------------------------------------------------

print("\nSummary Statistics")
print(df.describe())

# ----------------------------------------------------------
# Step 9 : Missing Values
# ----------------------------------------------------------

print("\nMissing Values")
print(df.isnull().sum())

# ----------------------------------------------------------
# Step 10 : Duplicate Records
# ----------------------------------------------------------

print("\nDuplicate Records")
print(df.duplicated().sum())

# ----------------------------------------------------------
# Step 11 : Unique Values
# ----------------------------------------------------------

print("\nUnique Values")

for column in df.columns:
    print(f"\n{column}")
    print(df[column].unique())

# ----------------------------------------------------------
# Step 12 : Heart Disease Distribution
# ----------------------------------------------------------

print("\nHeart Disease Count")
print(df["HeartDisease"].value_counts())

plt.figure(figsize=(6,4))
sns.countplot(x="HeartDisease", data=df)
plt.title("Heart Disease Distribution")
plt.xlabel("Heart Disease")
plt.ylabel("Number of Patients")
plt.show()

# ----------------------------------------------------------
# Step 13 : Gender Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
sns.countplot(x="Sex", data=df)
plt.title("Gender Distribution")
plt.show()

# ----------------------------------------------------------
# Step 14 : Chest Pain Type Distribution
# ----------------------------------------------------------

plt.figure(figsize=(7,4))
sns.countplot(x="ChestPainType", data=df)
plt.title("Chest Pain Type Distribution")
plt.show()

# ----------------------------------------------------------
# Step 15 : Age Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
plt.hist(df["Age"], bins=20)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

# ----------------------------------------------------------
# Step 16 : Cholesterol Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
plt.hist(df["Cholesterol"], bins=20)
plt.title("Cholesterol Distribution")
plt.xlabel("Cholesterol")
plt.ylabel("Frequency")
plt.show()

# ----------------------------------------------------------
# Step 17 : Resting Blood Pressure Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
plt.hist(df["RestingBP"], bins=20)
plt.title("Resting Blood Pressure Distribution")
plt.xlabel("RestingBP")
plt.ylabel("Frequency")
plt.show()

# ----------------------------------------------------------
# Step 18 : Maximum Heart Rate Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
plt.hist(df["MaxHR"], bins=20)
plt.title("Maximum Heart Rate Distribution")
plt.xlabel("MaxHR")
plt.ylabel("Frequency")
plt.show()

# ----------------------------------------------------------
# Step 19 : Encode Categorical Columns
# ----------------------------------------------------------

eda_df = df.copy()

label_encoder = LabelEncoder()

categorical_columns = [
    "Sex",
    "ChestPainType",
    "RestingECG",
    "ExerciseAngina",
    "ST_Slope"
]

for column in categorical_columns:
    eda_df[column] = label_encoder.fit_transform(eda_df[column])

# ----------------------------------------------------------
# Step 20 : Correlation Matrix
# ----------------------------------------------------------

print("\nCorrelation Matrix")
print(eda_df.corr())

# ----------------------------------------------------------
# Step 21 : Correlation Heatmap
# ----------------------------------------------------------

plt.figure(figsize=(12,8))

sns.heatmap(
    eda_df.corr(),
    annot=True,
    cmap="coolwarm",
    linewidths=0.5
)

plt.title("Correlation Heatmap")
plt.show()

# ----------------------------------------------------------
# Step 22 : Pair Plot
# ----------------------------------------------------------

sns.pairplot(
    eda_df,
    hue="HeartDisease",
    diag_kind="hist"
)

plt.show()

# ----------------------------------------------------------
# Step 23 : Heart Disease vs Gender
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
sns.countplot(x="Sex", hue="HeartDisease", data=df)
plt.title("Heart Disease vs Gender")
plt.show()

# ----------------------------------------------------------
# Step 24 : Heart Disease vs Chest Pain Type
# ----------------------------------------------------------

plt.figure(figsize=(8,4))
sns.countplot(x="ChestPainType", hue="HeartDisease", data=df)
plt.title("Heart Disease vs Chest Pain Type")
plt.show()

# ----------------------------------------------------------
# Step 25 : Heart Disease vs Exercise Angina
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
sns.countplot(x="ExerciseAngina", hue="HeartDisease", data=df)
plt.title("Heart Disease vs Exercise Angina")
plt.show()

# ----------------------------------------------------------
# Step 26 : Heart Disease vs ST_Slope
# ----------------------------------------------------------

plt.figure(figsize=(7,4))
sns.countplot(x="ST_Slope", hue="HeartDisease", data=df)
plt.title("Heart Disease vs ST_Slope")
plt.show()

# ----------------------------------------------------------
# Step 27 : Box Plot - Age
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
sns.boxplot(x=df["Age"])
plt.title("Age Box Plot")
plt.show()

# ----------------------------------------------------------
# Step 28 : Box Plot - Cholesterol
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
sns.boxplot(x=df["Cholesterol"])
plt.title("Cholesterol Box Plot")
plt.show()

# ----------------------------------------------------------
# Step 29 : Box Plot - Resting Blood Pressure
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
sns.boxplot(x=df["RestingBP"])
plt.title("Resting Blood Pressure Box Plot")
plt.show()

# ----------------------------------------------------------
# Step 30 : Box Plot - Maximum Heart Rate
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
sns.boxplot(x=df["MaxHR"])
plt.title("Maximum Heart Rate Box Plot")
plt.show()

# ----------------------------------------------------------
# Step 31 : Outlier Detection using IQR
# ----------------------------------------------------------

print("\nOutlier Detection")

numerical_columns = [
    "Age",
    "RestingBP",
    "Cholesterol",
    "MaxHR",
    "Oldpeak"
]

for column in numerical_columns:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower) |
        (df[column] > upper)
    ]

    print(f"{column} : {len(outliers)} Outliers")


print("\nSkewness")
print(df.skew(numeric_only=True))

print("\nKurtosis")
print(df.kurt(numeric_only=True))


print("\n" + "=" * 60)
print("PHASE 5 COMPLETED SUCCESSFULLY")
print("Exploratory Data Analysis Completed")
print("All Charts Generated Successfully")
print("=" * 60)