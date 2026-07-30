import requests
import pandas as pd
import time

URL = "http://127.0.0.1:5000/predict"

print("🚀 INITIATING DEEP DIAGNOSTIC TEST SUITE...\n")

# Baseline valid payload to modify for tests
base_payload = {
    "Age": 45, "Sex": "M", "ChestPainType": "ATA", "RestingBP": 120,
    "Cholesterol": 200, "FastingBS": 0, "RestingECG": "Normal",
    "MaxHR": 150, "ExerciseAngina": "N", "Oldpeak": 0.0, "ST_Slope": "Up"
}


def check_error(test_name, payload, expected_error):
    try:
        response = requests.post(URL, data=payload)
        if expected_error in response.text or "Error" in response.text or "failed" in response.text.lower():
            print(f"✅ PASSED | {test_name}")
        else:
            print(f"❌ FAILED | {test_name} (Server accepted bad data!)")
    except Exception as e:
        print(f"⚠️ ERROR | Connection failed: {e}")


# ==========================================
# PHASE 1: EXACT BOUNDARY & TYPE TESTING
# ==========================================
print("--- PHASE 1: VULNERABILITY & BOUNDARY ATTACKS ---")

# Test exactly 1 over the limit
payload_age_high = base_payload.copy()
payload_age_high["Age"] = 121
check_error("Boundary Attack: Age 121", payload_age_high, "Age must be")

# Test exactly 1 under the limit
payload_bp_low = base_payload.copy()
payload_bp_low["RestingBP"] = 49
check_error("Boundary Attack: BP 49", payload_bp_low, "Blood Pressure must be")

# Test Type Mismatch (String instead of Int)
payload_type_error = base_payload.copy()
payload_type_error["Cholesterol"] = "Two Hundred"
check_error("Type Attack: String in Number Field", payload_type_error, "invalid literal")

# Test Missing Data (Simulating a bypassed required tag)
payload_missing = base_payload.copy()
del payload_missing["MaxHR"]
check_error("Missing Data Attack: Deleted MaxHR Field", payload_missing, "NoneType")

# ==========================================
# PHASE 2: MASS INTEGRATION & ACCURACY TEST
# ==========================================
print("\n--- PHASE 2: MASS DATASET INTEGRATION TEST ---")
try:
    df = pd.read_csv(
        r"C:\Users\Tanmay\OneDrive\Desktop\Heart disease risk prediction\Project Plan\00 - Dataset\heart.csv")
    # Grab 50 random patients
    sample_df = df.sample(n=50, random_state=42)

    correct_predictions = 0
    total_time = 0

    print("Firing 50 real patients at the Flask server...")

    for index, row in sample_df.iterrows():
        # Convert pandas row to dictionary payload
        patient_data = row.drop("HeartDisease").to_dict()
        actual_disease = row["HeartDisease"]  # 1 is High Risk, 0 is Low Risk

        start_time = time.time()
        response = requests.post(URL, data=patient_data)
        end_time = time.time()

        total_time += (end_time - start_time)

        # Check if the server predicted correctly
        if actual_disease == 1 and "High Risk" in response.text:
            correct_predictions += 1
        elif actual_disease == 0 and "Low Risk" in response.text:
            correct_predictions += 1

    accuracy = (correct_predictions / 50) * 100
    avg_speed = (total_time / 50) * 1000  # in milliseconds

    print(f"\n📊 RESULTS: Mass Testing Complete!")
    print(f"Server Accuracy on 50 random patients: {accuracy}%")
    print(f"Average Server Response Time: {avg_speed:.2f} milliseconds per patient")

except FileNotFoundError:
    print("⚠️ ERROR: Could not find 'heart.csv' to run mass testing.")
except Exception as e:
    print(f"⚠️ ERROR during mass test: {e}")