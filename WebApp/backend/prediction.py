# ==========================================================
# HEART DISEASE RISK PREDICTION
# Prediction Module
# ==========================================================

import joblib
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "heart_disease_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("Heart Disease Model Loaded Successfully.")
except Exception as e:
    print(f"Error Loading Model: {e}")
    model = None


# ==========================================================
# Prediction Function
# ==========================================================

def predict_heart_disease(input_data):
    """
    Predict Heart Disease

    Parameters:
        input_data (list): List of 11 feature values

    Returns:
        dict: Prediction result
    """

    if model is None:
        return {
            "success": False,
            "prediction": None,
            "message": "Model is not loaded."
        }

    try:

        # Convert input into NumPy array
        input_array = np.array(input_data, dtype=float).reshape(1, -1)

        # Validate feature count
        expected_features = getattr(model, "n_features_in_", input_array.shape[1])

        if input_array.shape[1] != expected_features:
            return {
                "success": False,
                "prediction": None,
                "message": f"Expected {expected_features} features but received {input_array.shape[1]}."
            }

        # Make prediction
        prediction = model.predict(input_array)[0]

        # Probability (if supported)
        probability = None
        if hasattr(model, "predict_proba"):
            probability = float(np.max(model.predict_proba(input_array)))

        # Convert prediction to readable text
        if prediction == 1:
            result = "Heart Disease Detected"
        else:
            result = "No Heart Disease Detected"

        return {
            "success": True,
            "prediction": int(prediction),
            "result": result,
            "confidence": probability
        }

    except Exception as e:

        return {
            "success": False,
            "prediction": None,
            "message": str(e)
        }


# ==========================================================
# Test Prediction
# ==========================================================

if __name__ == "__main__":

    sample_patient = [
        40,     # Age
        1,      # Sex
        1,      # ChestPainType
        140,    # RestingBP
        289,    # Cholesterol
        0,      # FastingBS
        1,      # RestingECG
        172,    # MaxHR
        0,      # ExerciseAngina
        0.0,    # Oldpeak
        2       # ST_Slope
    ]

    output = predict_heart_disease(sample_patient)

    print("\nPrediction Result")
    print(output)