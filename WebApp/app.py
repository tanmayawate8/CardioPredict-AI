# ==========================================================
# HEART DISEASE RISK PREDICTION
# Flask Application
# ==========================================================

from flask import Flask, render_template, request
from backend.prediction import predict_heart_disease

# ==========================================================
# Create Flask App
# ==========================================================

app = Flask(__name__)

# ==========================================================
# Home Page
# ==========================================================

@app.route("/")
def home():
    return render_template("index.html")

# ==========================================================
# About Page
# ==========================================================

@app.route("/about")
def about():
    return render_template("about.html")

# ==========================================================
# Contact Page
# ==========================================================

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ==========================================================
# Prediction Page
# ==========================================================

@app.route("/prediction")
def prediction_page():
    return render_template("prediction.html")

# ==========================================================
# Predict Heart Disease
# ==========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ----------------------------------------
        # Read Data from HTML Form
        # ----------------------------------------

        age = request.form["Age"]
        sex = request.form["Sex"]
        chest_pain = request.form["ChestPainType"]
        resting_bp = request.form["RestingBP"]
        cholesterol = request.form["Cholesterol"]
        fasting_bs = request.form["FastingBS"]
        resting_ecg = request.form["RestingECG"]
        max_hr = request.form["MaxHR"]
        exercise_angina = request.form["ExerciseAngina"]
        oldpeak = request.form["Oldpeak"]
        st_slope = request.form["ST_Slope"]

        # ----------------------------------------
        # Create Dictionary
        # ----------------------------------------

        patient_data = {

            "Age": age,
            "Sex": sex,
            "ChestPainType": chest_pain,
            "RestingBP": resting_bp,
            "Cholesterol": cholesterol,
            "FastingBS": fasting_bs,
            "RestingECG": resting_ecg,
            "MaxHR": max_hr,
            "ExerciseAngina": exercise_angina,
            "Oldpeak": oldpeak,
            "ST_Slope": st_slope

        }

        # ----------------------------------------
        # Predict
        # ----------------------------------------

        result = predict_heart_disease(patient_data)

        return render_template(

            "prediction.html",

            prediction=result["result"],

            confidence=result.get("confidence", None)

        )

    except Exception as e:

        return render_template(

            "prediction.html",

            prediction="Prediction Failed",

            error=str(e)

        )

# ==========================================================
# Run Flask Server
# ==========================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )