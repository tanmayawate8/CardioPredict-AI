# ============================================================
# HEART DISEASE RISK PREDICTION SYSTEM
# FLASK BACKEND
# ============================================================

# ============================================================
# IMPORTS
# ============================================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

import pandas as pd
import pickle
from pathlib import Path
import os
import resend

from config import Config
from extensions import db, login_manager
from models import User, Prediction


# ============================================================
# CREATE FLASK APPLICATION
# ============================================================

app = Flask(__name__)

# Load configuration
app.config.from_object(Config)


# ============================================================
# INITIALIZE EXTENSIONS
# ============================================================

db.init_app(app)

login_manager.init_app(app)


# ============================================================
# LOGIN MANAGER CONFIGURATION
# ============================================================

@login_manager.user_loader
def load_user(user_id):

    try:

        return db.session.get(
            User,
            int(user_id)
        )

    except (ValueError, TypeError):

        return None


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

with app.app_context():

    db.create_all()


# ============================================================
# RESEND EMAIL CONFIGURATION
# ============================================================

RESEND_API_KEY = os.getenv(
    "RESEND_API_KEY"
)

if RESEND_API_KEY:

    resend.api_key = RESEND_API_KEY

else:

    print(
        "WARNING: RESEND_API_KEY is not configured."
    )


# ============================================================
# LOAD TRAINED MACHINE LEARNING MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = (
    BASE_DIR /
    "heart_disease_model.pkl"
)


if not MODEL_PATH.exists():

    raise FileNotFoundError(

        f"Model file not found: {MODEL_PATH}"

    )


with open(
    MODEL_PATH,
    "rb"
) as file:

    model = pickle.load(file)


print(
    "Machine Learning Model Loaded Successfully"
)

print(
    "Model Path:",
    MODEL_PATH
)


# ============================================================
# LABEL ENCODING DICTIONARIES
# ============================================================

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


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# ABOUT PAGE
# ============================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# ============================================================
# CONTACT PAGE
# ============================================================

@app.route(
    "/contact",
    methods=["GET", "POST"]
)
def contact():

    if request.method == "POST":

        try:

            # --------------------------------------------
            # GET FORM DATA
            # --------------------------------------------

            name = request.form.get(
                "name",
                ""
            ).strip()

            email = request.form.get(
                "email",
                ""
            ).strip()

            subject = request.form.get(
                "subject",
                ""
            ).strip()

            message = request.form.get(
                "message",
                ""
            ).strip()


            # --------------------------------------------
            # VALIDATE FORM
            # --------------------------------------------

            if not name or not email or not message:

                return render_template(

                    "contact.html",

                    error=(
                        "Please fill in all required fields."
                    )

                )


            # --------------------------------------------
            # CHECK RESEND API KEY
            # --------------------------------------------

            if not RESEND_API_KEY:

                return render_template(

                    "contact.html",

                    error=(
                        "Email service is not configured. "
                        "Please try again later."
                    )

                )


            # --------------------------------------------
            # EMAIL PARAMETERS
            # --------------------------------------------

            params = {

                "from":
                "onboarding@resend.dev",

                "to":
                [
                    "codewithtanmay098@gmail.com"
                ],

                "subject":
                (
                    "Heart Disease Prediction Contact: "
                    f"{subject}"
                ),

                "html":
                f"""
                <h2>New Contact Form Submission</h2>

                <p>
                    <strong>Name:</strong>
                    {name}
                </p>

                <p>
                    <strong>Email:</strong>
                    {email}
                </p>

                <p>
                    <strong>Subject:</strong>
                    {subject}
                </p>

                <hr>

                <p>
                    <strong>Message:</strong>
                </p>

                <p>
                    {message}
                </p>

                <hr>

                <p>
                    Sent from CardioPredict AI
                </p>
                """

            }


            # --------------------------------------------
            # SEND EMAIL
            # --------------------------------------------

            resend.Emails.send(
                params
            )


            # --------------------------------------------
            # SUCCESS
            # --------------------------------------------

            return render_template(

                "contact.html",

                success=(
                    "Your message has been "
                    "sent successfully."
                )

            )


        except Exception as e:

            print(
                "CONTACT EMAIL ERROR:",
                str(e)
            )

            return render_template(

                "contact.html",

                error=str(e)

            )


    return render_template(
        "contact.html"
    )


# ==========================================
# REGISTER
# ==========================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    # --------------------------------------
    # IF ALREADY LOGGED IN
    # --------------------------------------

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )

    # --------------------------------------
    # POST REQUEST
    # --------------------------------------

    if request.method == "POST":

        # --------------------------------------
        # GET FORM DATA
        # --------------------------------------

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        # --------------------------------------
        # VALIDATE REQUIRED FIELDS
        # --------------------------------------

        if not username or not email or not password:

            return render_template(
                "register.html",
                error="Please fill in all fields."
            )

        # --------------------------------------
        # VALIDATE PASSWORD
        # --------------------------------------

        if password != confirm_password:

            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        # --------------------------------------
        # PASSWORD LENGTH
        # --------------------------------------

        if len(password) < 6:

            return render_template(
                "register.html",
                error=(
                    "Password must be at least "
                    "6 characters long."
                )
            )

        # --------------------------------------
        # CHECK EXISTING USER
        # --------------------------------------

        existing_user = User.query.filter(

            (User.username == username)
            |
            (User.email == email)

        ).first()

        if existing_user:

            return render_template(

                "register.html",

                error=(
                    "Username or email is "
                    "already registered."
                )

            )

        # --------------------------------------
        # CREATE NEW USER
        # --------------------------------------

        new_user = User(

            username=username,

            email=email

        )

        # --------------------------------------
        # HASH PASSWORD
        # --------------------------------------

        new_user.set_password(
            password
        )

        # --------------------------------------
        # SAVE USER TO DATABASE
        # --------------------------------------

        try:

            db.session.add(
                new_user
            )

            db.session.commit()

        except Exception as e:

            db.session.rollback()

            return render_template(

                "register.html",

                error=(
                    "Registration failed. "
                    "Please try again."
                )

            )

        # --------------------------------------
        # DO NOT AUTO LOGIN
        # --------------------------------------
        #
        # IMPORTANT:
        # We intentionally do NOT use:
        #
        # login_user(new_user)
        #
        # The user must login manually
        # after successful registration.
        #

        # --------------------------------------
        # SUCCESS MESSAGE
        # --------------------------------------

        flash(

            "Registration successful! "
            "Your account has been created. "
            "Please login to continue.",

            "success"

        )

        # --------------------------------------
        # REDIRECT TO LOGIN PAGE
        # --------------------------------------

        return redirect(

            url_for(
                "login"
            )

        )

    # --------------------------------------
    # GET REQUEST
    # --------------------------------------

    return render_template(

        "register.html"

    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # --------------------------------------------
    # ALREADY LOGGED IN
    # --------------------------------------------

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )


    # --------------------------------------------
    # POST REQUEST
    # --------------------------------------------

    if request.method == "POST":

        identifier = request.form.get(

            "identifier",

            ""

        ).strip().lower()


        password = request.form.get(

            "password",

            ""

        )


        remember = bool(

            request.form.get(
                "remember"
            )

        )


        # --------------------------------------------
        # FIND USER
        # --------------------------------------------

        user = User.query.filter(

            (User.username == identifier)
            |
            (User.email == identifier)

        ).first()


        # --------------------------------------------
        # VALIDATE LOGIN
        # --------------------------------------------

        if (

            user is None

            or not user.check_password(
                password
            )

        ):

            return render_template(

                "login.html",

                error=(

                    "Invalid username/email "
                    "or password."

                )

            )


        # --------------------------------------------
        # LOGIN USER
        # --------------------------------------------

        login_user(

            user,

            remember=remember

        )


        flash(

            f"Welcome back, {user.username}!",

            "success"

        )


        # --------------------------------------------
        # CHECK PENDING PREDICTION
        # --------------------------------------------

        if session.get(
            "pending_prediction"
        ):

            return redirect(

                url_for(
                    "save_pending_prediction"
                )

            )


        # --------------------------------------------
        # NORMAL LOGIN
        # --------------------------------------------

        return redirect(

            url_for(
                "dashboard"
            )

        )


    # --------------------------------------------
    # GET REQUEST
    # --------------------------------------------

    return render_template(
        "login.html"
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route(
    "/dashboard"
)
@login_required
def dashboard():

    predictions = Prediction.query.filter_by(

        user_id=current_user.id

    ).order_by(

        Prediction.created_at.desc()

    ).all()


    return render_template(

        "dashboard.html",

        predictions=predictions

    )

@app.route("/report/<int:prediction_id>")
@login_required
def view_report(prediction_id):

    prediction = Prediction.query.filter_by(
        id=prediction_id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "report.html",
        prediction=prediction
    )
# ============================================================
# PREDICTION PAGE
# ============================================================

@app.route(
    "/prediction"
)
def prediction_page():

    return render_template(
        "prediction.html"
    )


# ============================================================
# MAKE HEART DISEASE PREDICTION
# ============================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    try:

        # ====================================================
        # GET FORM VALUES
        # ====================================================

        Age = int(
            request.form.get(
                "Age"
            )
        )


        Sex_original = request.form.get(
            "Sex"
        )


        ChestPainType_original = request.form.get(
            "ChestPainType"
        )


        RestingBP = int(
            request.form.get(
                "RestingBP"
            )
        )


        Cholesterol = int(
            request.form.get(
                "Cholesterol"
            )
        )


        FastingBS = int(
            request.form.get(
                "FastingBS"
            )
        )


        RestingECG_original = request.form.get(
            "RestingECG"
        )


        MaxHR = int(
            request.form.get(
                "MaxHR"
            )
        )


        ExerciseAngina_original = request.form.get(
            "ExerciseAngina"
        )


        Oldpeak = float(
            request.form.get(
                "Oldpeak"
            )
        )


        ST_Slope_original = request.form.get(
            "ST_Slope"
        )


        # ====================================================
        # VALIDATE CATEGORICAL INPUTS
        # ====================================================

        if Sex_original not in sex_map:

            raise ValueError(
                "Invalid gender selected."
            )


        if ChestPainType_original not in cp_map:

            raise ValueError(
                "Invalid chest pain type selected."
            )


        if RestingECG_original not in ecg_map:

            raise ValueError(
                "Invalid resting ECG selected."
            )


        if ExerciseAngina_original not in angina_map:

            raise ValueError(
                "Invalid exercise angina value."
            )


        if ST_Slope_original not in slope_map:

            raise ValueError(
                "Invalid ST slope selected."
            )


        # ====================================================
        # ENCODE CATEGORICAL VALUES
        # ====================================================

        Sex = sex_map[
            Sex_original
        ]


        ChestPainType = cp_map[
            ChestPainType_original
        ]


        RestingECG = ecg_map[
            RestingECG_original
        ]


        ExerciseAngina = angina_map[
            ExerciseAngina_original
        ]


        ST_Slope = slope_map[
            ST_Slope_original
        ]


        # ====================================================
        # CREATE MODEL INPUT DATAFRAME
        # ====================================================

        patient = pd.DataFrame(

            [[

                Age,

                Sex,

                ChestPainType,

                RestingBP,

                Cholesterol,

                FastingBS,

                RestingECG,

                MaxHR,

                ExerciseAngina,

                Oldpeak,

                ST_Slope

            ]],

            columns=[

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

                "ST_Slope"

            ]

        )


        # ====================================================
        # MACHINE LEARNING PREDICTION
        # ====================================================

        prediction_value = model.predict(

            patient

        )[0]


        # ====================================================
        # GET PREDICTION PROBABILITY
        # ====================================================

        if hasattr(
            model,
            "predict_proba"
        ):

            probabilities = model.predict_proba(

                patient

            )[0]


            # --------------------------------------------
            # IMPORTANT
            # Find probability of positive class
            # --------------------------------------------

            if hasattr(
                model,
                "classes_"
            ):

                classes = list(
                    model.classes_
                )


                if 1 in classes:

                    positive_index = classes.index(
                        1
                    )

                    confidence = float(

                        probabilities[
                            positive_index
                        ]

                    )

                else:

                    confidence = float(
                        probabilities[-1]
                    )

            else:

                confidence = float(
                    probabilities[-1]
                )

        else:

            confidence = float(
                prediction_value
            )


        # ====================================================
        # CONVERT RESULT TO TEXT
        # ====================================================

        if int(
            prediction_value
        ) == 1:

            result = "High Risk"

        else:

            result = "Low Risk"


        # ====================================================
        # HUMAN-READABLE PATIENT INFORMATION
        # ====================================================

        chest_pain_labels = {

            "ATA":
            "Atypical Angina (ATA)",

            "NAP":
            "Non-Anginal Pain (NAP)",

            "ASY":
            "Asymptomatic (ASY)",

            "TA":
            "Typical Angina (TA)"

        }


        patient_input = {

            "Age":
            Age,


            "Sex":

            (
                "Male"

                if Sex_original == "M"

                else "Female"
            ),


            "Chest Pain Type":

            chest_pain_labels[
                ChestPainType_original
            ],


            "Resting Blood Pressure":

            f"{RestingBP} mmHg",


            "Cholesterol":

            f"{Cholesterol} mg/dL",


            "Fasting Blood Sugar":

            (
                "Yes (> 120 mg/dL)"

                if FastingBS == 1

                else "No (≤ 120 mg/dL)"
            ),


            "Resting ECG":

            RestingECG_original,


            "Maximum Heart Rate":

            f"{MaxHR} bpm",


            "Exercise Induced Angina":

            (
                "Yes"

                if ExerciseAngina_original == "Y"

                else "No"
            ),


            "Oldpeak":

            Oldpeak,


            "ST Slope":

            ST_Slope_original

        }


        # ====================================================
        # SAVE PREDICTION IN SESSION
        # ====================================================

        session[
            "pending_prediction"
        ] = {

            "Age":
            Age,


            "Sex":

            (
                "Male"

                if Sex_original == "M"

                else "Female"
            ),


            "ChestPainType":

            chest_pain_labels[
                ChestPainType_original
            ],


            "RestingBP":
            RestingBP,


            "Cholesterol":
            Cholesterol,


            "FastingBS":

            (
                "Yes (> 120 mg/dL)"

                if FastingBS == 1

                else "No (≤ 120 mg/dL)"
            ),


            "RestingECG":
            RestingECG_original,


            "MaxHR":
            MaxHR,


            "ExerciseAngina":

            (
                "Yes"

                if ExerciseAngina_original == "Y"

                else "No"
            ),


            "Oldpeak":
            Oldpeak,


            "ST_Slope":
            ST_Slope_original,


            "result":
            result,


            "probability":

            round(

                confidence * 100,

                2

            )

        }


        # ====================================================
        # RENDER RESULT
        # ====================================================

        return render_template(

            "prediction.html",

            prediction=result,

            confidence=confidence,

            patient_input=patient_input

        )


    except Exception as e:

        # ====================================================
        # PRINT ERROR IN TERMINAL
        # ====================================================

        print(
            "PREDICTION ERROR:",
            str(e)
        )


        # ====================================================
        # SHOW ERROR ON PAGE
        # ====================================================

        return render_template(

            "prediction.html",

            error=(

                "Prediction failed: "

                + str(e)

            )

        )


# ============================================================
# SAVE PREDICTION
# ============================================================

@app.route(
    "/save-prediction",
    methods=["POST"]
)
def save_prediction():

    # --------------------------------------------
    # CHECK PENDING PREDICTION
    # --------------------------------------------

    if not session.get(
        "pending_prediction"
    ):

        flash(

            "No prediction available to save.",

            "error"

        )

        return redirect(

            url_for(
                "prediction_page"
            )

        )


    # --------------------------------------------
    # USER NOT LOGGED IN
    # --------------------------------------------

    if not current_user.is_authenticated:

        flash(

            "Please login or register "
            "to save your prediction.",

            "info"

        )

        return redirect(

            url_for(
                "login"
            )

        )


    # --------------------------------------------
    # USER LOGGED IN
    # --------------------------------------------

    return redirect(

        url_for(
            "save_pending_prediction"
        )

    )


# ============================================================
# SAVE PENDING PREDICTION TO DATABASE
# ============================================================

@app.route(
    "/save-pending-prediction"
)
@login_required
def save_pending_prediction():

    # --------------------------------------------
    # GET PENDING PREDICTION
    # --------------------------------------------

    pending = session.get(

        "pending_prediction"

    )


    # --------------------------------------------
    # CHECK PENDING DATA
    # --------------------------------------------

    if not pending:

        flash(

            "No prediction found to save.",

            "error"

        )

        return redirect(

            url_for(
                "dashboard"
            )

        )


    try:

        # --------------------------------------------
        # CREATE DATABASE RECORD
        # --------------------------------------------

        new_prediction = Prediction(

            user_id=current_user.id,

            age=pending["Age"],

            sex=pending["Sex"],

            chest_pain_type=
            pending["ChestPainType"],

            resting_bp=
            pending["RestingBP"],

            cholesterol=
            pending["Cholesterol"],

            fasting_bs=
            pending["FastingBS"],

            resting_ecg=
            pending["RestingECG"],

            max_hr=
            pending["MaxHR"],

            exercise_angina=
            pending["ExerciseAngina"],

            oldpeak=
            pending["Oldpeak"],

            st_slope=
            pending["ST_Slope"],

            result=
            pending["result"],

            probability=
            pending["probability"]

        )


        # --------------------------------------------
        # SAVE DATABASE RECORD
        # --------------------------------------------

        db.session.add(

            new_prediction

        )

        db.session.commit()


        # --------------------------------------------
        # REMOVE SESSION DATA
        # --------------------------------------------

        session.pop(

            "pending_prediction",

            None

        )


        # --------------------------------------------
        # SUCCESS MESSAGE
        # --------------------------------------------

        flash(

            "Prediction saved successfully!",

            "success"

        )


        # --------------------------------------------
        # DASHBOARD
        # --------------------------------------------

        return redirect(

            url_for(
                "dashboard"
            )

        )


    except Exception as e:

        # --------------------------------------------
        # ROLLBACK DATABASE
        # --------------------------------------------

        db.session.rollback()


        print(

            "SAVE PREDICTION ERROR:",

            str(e)

        )


        flash(

            "Unable to save prediction: "
            + str(e),

            "error"

        )


        return redirect(

            url_for(
                "prediction_page"
            )

        )


# ============================================================
# LOGOUT
# ============================================================

@app.route(
    "/logout"
)
@login_required
def logout():

    logout_user()


    flash(

        "You have been logged out.",

        "success"

    )


    # --------------------------------------------
    # FIXED TYPO:
    # dashboard, NOT dasboard
    # --------------------------------------------

    return redirect(

        url_for(
            "dashboard"
        )

    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )