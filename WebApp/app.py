# ==========================================
# HEART DISEASE RISK PREDICTION
# FLASK BACKEND
# ==========================================

from flask import Flask, render_template, request
import pandas as pd
import pickle
from pathlib import Path


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)


# ==========================================
# LOAD TRAINED MODEL
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "heart_disease_model.pkl"

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

print("Model Loaded Successfully")


# ==========================================
# LABEL ENCODING DICTIONARIES
# ==========================================

sex_map = {
    "M": 1,
    "F": 0
}


cp_map = {
    "ATA": 0,
    "NAP": 1,
    "ASY": 2,
    "TA": 3
}


ecg_map = {
    "Normal": 1,
    "ST": 2,
    "LVH": 0
}


angina_map = {
    "N": 0,
    "Y": 1
}


slope_map = {
    "Up": 2,
    "Flat": 1,
    "Down": 0
}


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# ABOUT PAGE
# ==========================================

@app.route("/about")
def about():

    return render_template("about.html")


# ==========================================
# CONTACT PAGE
# ==========================================

@app.route("/contact")
def contact():

    return render_template("contact.html")


# ==========================================
# PREDICTION PAGE
# ==========================================

@app.route("/prediction")
def prediction_page():

    return render_template("prediction.html")


# ==========================================
# PREDICT ROUTE
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ==========================================
        # GET ORIGINAL USER INPUT VALUES
        # ==========================================

        Age = int(request.form["Age"])

        Sex_original = request.form["Sex"]

        ChestPainType_original = request.form["ChestPainType"]

        RestingBP = int(request.form["RestingBP"])

        Cholesterol = int(request.form["Cholesterol"])

        FastingBS = int(request.form["FastingBS"])

        RestingECG_original = request.form["RestingECG"]

        MaxHR = int(request.form["MaxHR"])

        ExerciseAngina_original = request.form["ExerciseAngina"]

        Oldpeak = float(request.form["Oldpeak"])

        ST_Slope_original = request.form["ST_Slope"]


        # ==========================================
        # ENCODE INPUT VALUES FOR MODEL
        # ==========================================

        Sex = sex_map[Sex_original]

        ChestPainType = cp_map[ChestPainType_original]

        RestingECG = ecg_map[RestingECG_original]

        ExerciseAngina = angina_map[ExerciseAngina_original]

        ST_Slope = slope_map[ST_Slope_original]


        # ==========================================
        # CREATE DATAFRAME FOR MODEL
        # ==========================================

        patient = pd.DataFrame([{

            "Age": Age,

            "Sex": Sex,

            "ChestPainType": ChestPainType,

            "RestingBP": RestingBP,

            "Cholesterol": Cholesterol,

            "FastingBS": FastingBS,

            "RestingECG": RestingECG,

            "MaxHR": MaxHR,

            "ExerciseAngina": ExerciseAngina,

            "Oldpeak": Oldpeak,

            "ST_Slope": ST_Slope

        }])


        # ==========================================
        # MAKE PREDICTION
        # ==========================================

        prediction_value = model.predict(patient)[0]


        # ==========================================
        # GET MODEL PROBABILITY
        # ==========================================

        probabilities = model.predict_proba(patient)[0]


        # ==========================================
        # GET PROBABILITY OF POSITIVE CLASS
        #
        # Assumption:
        # 0 = No Heart Disease
        # 1 = Heart Disease
        # ==========================================

        confidence = float(probabilities[1])


        # ==========================================
        # CONVERT MODEL OUTPUT
        # TO HIGH RISK / LOW RISK
        # ==========================================

        if prediction_value == 1:

            result = "High Risk"

        else:

            result = "Low Risk"


        # ==========================================
        # PATIENT INPUT VALUES FOR RESULT SECTION
        #
        # These are the original human-readable
        # values entered by the user.
        # ==========================================

        patient_input = {

            "Age": Age,

            "Sex": (
                "Male"
                if Sex_original == "M"
                else "Female"
            ),

            "Chest Pain Type": {
                "ATA": "Atypical Angina (ATA)",
                "NAP": "Non-Anginal Pain (NAP)",
                "ASY": "Asymptomatic (ASY)",
                "TA": "Typical Angina (TA)"
            }[ChestPainType_original],

            "Resting Blood Pressure": (
                f"{RestingBP} mmHg"
            ),

            "Cholesterol": (
                f"{Cholesterol} mg/dL"
            ),

            "Fasting Blood Sugar": (
                "Yes (> 120 mg/dL)"
                if FastingBS == 1
                else "No (≤ 120 mg/dL)"
            ),

            "Resting ECG": RestingECG_original,

            "Maximum Heart Rate": (
                f"{MaxHR} bpm"
            ),

            "Exercise Induced Angina": (
                "Yes"
                if ExerciseAngina_original == "Y"
                else "No"
            ),

            "Oldpeak": Oldpeak,

            "ST Slope": ST_Slope_original

        }


        # ==========================================
        # SEND RESULT TO PREDICTION.HTML
        # ==========================================

        return render_template(

            "prediction.html",

            prediction=result,

            confidence=confidence,

            patient_input=patient_input

        )


    # ==========================================
    # ERROR HANDLING
    # ==========================================

    except Exception as e:

        return render_template(

            "prediction.html",

            error=str(e)

        )


# ==========================================
# RUN FLASK APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )