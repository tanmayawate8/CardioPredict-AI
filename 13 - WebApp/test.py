import requests

# Explicitly target the POST route
URL = "http://127.0.0.1:5000/predict"

print("Starting Final Security & AI Tests...\n")

# TEST 1: Ground Truth 0 (Should be Low Risk)
low_risk_payload = {
    "Age": 40, "Sex": "M", "ChestPainType": "ATA", "RestingBP": 140,
    "Cholesterol": 289, "FastingBS": 0, "RestingECG": "Normal",
    "MaxHR": 172, "ExerciseAngina": "N", "Oldpeak": 0.0, "ST_Slope": "Up"
}

# TEST 2: Ground Truth 1 (Should be High Risk)
high_risk_payload = {
    "Age": 48, "Sex": "F", "ChestPainType": "ASY", "RestingBP": 138,
    "Cholesterol": 214, "FastingBS": 0, "RestingECG": "Normal",
    "MaxHR": 108, "ExerciseAngina": "Y", "Oldpeak": 1.5, "ST_Slope": "Flat"
}

# TEST 3: Malicious Data Attack
hack_payload = {
    "Age": -500, "Sex": "M", "ChestPainType": "ATA", "RestingBP": 9999,
    "Cholesterol": 289, "FastingBS": 0, "RestingECG": "Normal",
    "MaxHR": 172, "ExerciseAngina": "N", "Oldpeak": 0.0, "ST_Slope": "Up"
}

def run_test(name, payload, success_keyword):
    try:
        response = requests.post(URL, data=payload)
        if success_keyword in response.text:
            print(f"PASSED | {name}")
        else:
            print(f"FAILED | {name}")
            print(f"   -> Expected '{success_keyword}' but server did something else.")
    except Exception as e:
        print(f"⚠️ ERROR | Could not connect: {e}")

run_test("AI Test 1: Low Risk Detection", low_risk_payload, "Low Risk")
run_test("AI Test 2: High Risk Detection", high_risk_payload, "High Risk")
# If the security fix worked, the server will catch the -500 age and return the ValueError text!
run_test("Security Test: Blocking Impossible Data", hack_payload, "Age must be between 1 and 120")

print("\nTesting Complete.")