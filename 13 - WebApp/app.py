# ============================================================
# HEART DISEASE RISK PREDICTION SYSTEM
# FLASK BACKEND - FULLY OPTIMIZED & SECURED
# ============================================================

from flask import (
    Flask, render_template, request, redirect, url_for, flash, session
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)
import pandas as pd
import pickle
from pathlib import Path
import os
import secrets
import string

# Import Authlib for Google Login and ProxyFix for Render Deployment
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from extensions import db, login_manager
from models import User, Prediction

# ============================================================
# CREATE FLASK APPLICATION
# ============================================================
app = Flask(__name__)

# Tell Flask it is behind a proxy (like Render) to fix HTTPS redirects
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config.from_object(Config)

# Add Google OAuth Credentials (Preserved as requested)
app.config['GOOGLE_CLIENT_ID'] = "472208823648-hqal3kdqbbi8igap3trjvncqordu0vb0.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"

# ============================================================
# INITIALIZE EXTENSIONS & OAUTH
# ============================================================
db.init_app(app)
login_manager.init_app(app)

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config.get('GOOGLE_CLIENT_ID'),
    client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (ValueError, TypeError):
        return None


with app.app_context():
    db.create_all()

# ============================================================
# LOAD AI MODEL, SCALER, AND ENCODERS
# ============================================================
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "heart_disease_model.pkl"
SCALER_PATH = BASE_DIR / "scaler.pkl"
ENCODERS_PATH = BASE_DIR / "label_encoders.pkl"

if not MODEL_PATH.exists() or not SCALER_PATH.exists() or not ENCODERS_PATH.exists():
    raise FileNotFoundError("Missing one or more required .pkl files in the WebApp folder!")

# Load Model
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

# Load Scaler
with open(SCALER_PATH, "rb") as file:
    scaler = pickle.load(file)

# Load Label Encoders
with open(ENCODERS_PATH, "rb") as file:
    encoders = pickle.load(file)

print("AI Model, Scaler, and Encoders Loaded Successfully")

# Dynamically extract the exact valid categories the model was trained on
valid_sex = list(encoders['Sex'].classes_)
valid_cp = list(encoders['ChestPainType'].classes_)
valid_ecg = list(encoders['RestingECG'].classes_)
valid_angina = list(encoders['ExerciseAngina'].classes_)
valid_slope = list(encoders['ST_Slope'].classes_)


# ============================================================
# HOME PAGE
# ============================================================
@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# ABOUT PAGE
# ============================================================
@app.route("/about")
def about():
    return render_template("about.html")


# ============================================================
# CONTACT PAGE
# ============================================================
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            subject = request.form.get("subject", "").strip()
            message = request.form.get("message", "").strip()

            if not name or not email or not message:
                flash("Please fill in all required fields.", "error")
                return render_template("contact.html")

            flash("Thank you! Your message has been sent successfully.", "success")
            return redirect(url_for("contact"))

        except Exception as e:
            flash(f"An error occurred while sending your message: {str(e)}", "error")

    return render_template("contact.html")


# ==========================================
# REGISTER (STANDARD)
# ==========================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password:
            return render_template("register.html", error="Please fill in all fields.")

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match.")

        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters long.")

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            return render_template("register.html", error="Username or email is already registered.")

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template("register.html", error="Registration failed. Please try again.")

        flash("Registration successful! Your account has been created. Please login to continue.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# ============================================================
# LOGIN (STANDARD)
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()

        if user is None or not user.check_password(password):
            return render_template("login.html", error="Invalid username/email or password.")

        login_user(user, remember=remember)
        flash(f"Welcome back, {user.username}!", "success")

        if session.get("pending_prediction"):
            return redirect(url_for("save_pending_prediction"))

        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ============================================================
# GOOGLE OAUTH LOGIN ROUTES
# ============================================================
@app.route('/login/google')
def google_login():
    # Save whether they clicked from 'login' or 'register' into the session
    session['google_action'] = request.args.get('action', 'login')

    redirect_uri = url_for('google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/login/google/authorize')
def google_authorize():
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')

        if not user_info:
            flash("Google login failed. Please try again.", "error")
            return redirect(url_for('login'))

        email = user_info.get('email').lower()
        name = user_info.get('name')

        user = User.query.filter_by(email=email).first()

        # Check the action we saved earlier
        action = session.get('google_action', 'login')

        # SCENARIO 1: ACCOUNT DOES NOT EXIST
        if not user:
            if action == 'login':
                # Block them and show the error message on the login page
                flash("Account does not exist. Please register first.", "error")
                return redirect(url_for('login'))
            else:
                # They clicked from Register, so send them to the setup page
                session['google_email'] = email
                session['google_name'] = name
                return redirect(url_for('google_setup'))

        # SCENARIO 2: ACCOUNT ALREADY EXISTS
        if action == 'register':
            flash(f"Account already exists! Welcome back, {user.username}.", "success")
        else:
            flash(f"Welcome back, {user.username}!", "success")

        # Log them in securely
        login_user(user, remember=True)

        # Handle pending predictions
        if session.get("pending_prediction"):
            return redirect(url_for("save_pending_prediction"))

        return redirect(url_for('dashboard'))

    except Exception as e:
        flash(f"Authentication failed: {str(e)}", "error")
        return redirect(url_for('login'))

# ============================================================
# GOOGLE ACCOUNT SETUP (PROFESSIONAL ONBOARDING)
# ============================================================
@app.route('/google-setup', methods=['GET', 'POST'])
def google_setup():
    # If they somehow got here without Google Auth, send them to register
    if 'google_email' not in session:
        return redirect(url_for('register'))

    email = session['google_email']
    name = session['google_name']

    # Auto-generate a clean suggested username (removes spaces from Google name)
    suggested_username = name.replace(" ", "")

    if request.method == 'POST':
        username = request.form.get('username').strip()

        if not username:
            return render_template('google_setup.html', email=email, suggested_username=suggested_username,
                                   error="Username is required.")

        # Check if they picked a username that someone else is already using
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('google_setup.html', email=email, suggested_username=username,
                                   error="Username is already taken. Please choose another.")

        # Generate a secure random password for Google-created accounts
        alphabet = string.ascii_letters + string.digits + string.punctuation
        random_password = ''.join(secrets.choice(alphabet) for i in range(20))

        new_user = User(username=username, email=email)
        new_user.set_password(random_password)

        db.session.add(new_user)
        db.session.commit()

        # Clear the setup session data
        session.pop('google_email', None)
        session.pop('google_name', None)

        # Log them in and finalize
        login_user(new_user, remember=True)
        flash("Account created successfully with Google!", "success")

        if session.get("pending_prediction"):
            return redirect(url_for("save_pending_prediction"))

        return redirect(url_for('dashboard'))

    return render_template('google_setup.html', email=email, suggested_username=suggested_username)

# ============================================================
# DASHBOARD
# ============================================================
@app.route("/dashboard")
@login_required
def dashboard():
    predictions = Prediction.query.filter_by(
        user_id=current_user.id
    ).order_by(Prediction.created_at.desc()).all()
    return render_template("dashboard.html", predictions=predictions)


# ============================================================
# UPDATE PROFILE
# ============================================================
@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()
    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    user = db.session.get(User, current_user.id)

    try:
        # Check and update Username
        if username and username != user.username:
            if User.query.filter_by(username=username).first():
                flash("Username is already taken.", "error")
                return redirect(url_for("dashboard"))
            user.username = username

        # Check and update Email
        if email and email != user.email:
            if User.query.filter_by(email=email).first():
                flash("Email is already registered.", "error")
                return redirect(url_for("dashboard"))
            user.email = email

        # Password Update Logic
        if current_password or new_password or confirm_password:
            if not current_password:
                flash("Please enter your current password to set a new one.", "error")
                return redirect(url_for("dashboard"))
            if not user.check_password(current_password):
                flash("Incorrect current password.", "error")
                return redirect(url_for("dashboard"))
            if new_password != confirm_password:
                flash("New passwords do not match.", "error")
                return redirect(url_for("dashboard"))
            if len(new_password) < 6:
                flash("New password must be at least 6 characters.", "error")
                return redirect(url_for("dashboard"))

            user.set_password(new_password)

        db.session.commit()
        flash("Profile updated successfully!", "success")

    except Exception as e:
        db.session.rollback()
        flash("An error occurred while updating your profile.", "error")

    return redirect(url_for("dashboard"))


# ============================================================
# DELETE ACCOUNT
# ============================================================
@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    user = db.session.get(User, current_user.id)
    try:
        Prediction.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()

        logout_user()
        flash("Your account and all associated data have been permanently deleted.", "success")
        return redirect(url_for("home"))

    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting your account.", "error")
        return redirect(url_for("dashboard"))


# ============================================================
# VIEW REPORT
# ============================================================
@app.route("/report/<int:prediction_id>")
@login_required
def view_report(prediction_id):
    prediction = Prediction.query.filter_by(
        id=prediction_id, user_id=current_user.id
    ).first_or_404()
    return render_template("report.html", prediction=prediction)


# ============================================================
# PREDICTION PAGE
# ============================================================
@app.route("/prediction")
def prediction_page():
    return render_template("prediction.html")


# ============================================================
# MAKE HEART DISEASE PREDICTION
# ============================================================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        Age = int(request.form.get("Age"))
        Sex_original = request.form.get("Sex")
        ChestPainType_original = request.form.get("ChestPainType")
        RestingBP = int(request.form.get("RestingBP"))
        Cholesterol = int(request.form.get("Cholesterol"))
        FastingBS = int(request.form.get("FastingBS"))
        RestingECG_original = request.form.get("RestingECG")
        MaxHR = int(request.form.get("MaxHR"))
        ExerciseAngina_original = request.form.get("ExerciseAngina")
        Oldpeak = float(request.form.get("Oldpeak"))
        ST_Slope_original = request.form.get("ST_Slope")

        if Sex_original not in valid_sex:
            raise ValueError("Invalid gender selected.")
        if ChestPainType_original not in valid_cp:
            raise ValueError("Invalid chest pain type selected.")
        if RestingECG_original not in valid_ecg:
            raise ValueError("Invalid resting ECG selected.")
        if ExerciseAngina_original not in valid_angina:
            raise ValueError("Invalid exercise angina value.")
        if ST_Slope_original not in valid_slope:
            raise ValueError("Invalid ST slope selected.")

        if not (1 <= Age <= 120):
            raise ValueError("Age must be between 1 and 120.")
        if not (50 <= RestingBP <= 300):
            raise ValueError("Resting Blood Pressure must be between 50 and 300 mmHg.")
        if not (0 <= Cholesterol <= 1000):
            raise ValueError("Cholesterol must be between 0 and 1000 mg/dL.")
        if not (50 <= MaxHR <= 250):
            raise ValueError("Maximum Heart Rate must be between 50 and 250 bpm.")
        if FastingBS not in [0, 1]:
            raise ValueError("Fasting Blood Sugar must be 0 or 1.")
        if not (-5.0 <= Oldpeak <= 10.0):
            raise ValueError("Oldpeak must be between -5.0 and 10.0.")

        Sex = encoders["Sex"].transform([Sex_original])[0]
        ChestPainType = encoders["ChestPainType"].transform([ChestPainType_original])[0]
        RestingECG = encoders["RestingECG"].transform([RestingECG_original])[0]
        ExerciseAngina = encoders["ExerciseAngina"].transform([ExerciseAngina_original])[0]
        ST_Slope = encoders["ST_Slope"].transform([ST_Slope_original])[0]

        patient = pd.DataFrame(
            [[Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG, MaxHR, ExerciseAngina, Oldpeak,
              ST_Slope]],
            columns=["Age", "Sex", "ChestPainType", "RestingBP", "Cholesterol", "FastingBS", "RestingECG", "MaxHR",
                     "ExerciseAngina", "Oldpeak", "ST_Slope"]
        )

        numerical_columns = ["Age", "RestingBP", "Cholesterol", "FastingBS", "MaxHR", "Oldpeak"]
        patient[numerical_columns] = scaler.transform(patient[numerical_columns])

        prediction_value = model.predict(patient)[0]

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(patient)[0]
            if hasattr(model, "classes_"):
                classes = list(model.classes_)
                if 1 in classes:
                    positive_index = classes.index(1)
                    confidence = float(probabilities[positive_index])
                else:
                    confidence = float(probabilities[-1])
            else:
                confidence = float(probabilities[-1])
        else:
            confidence = float(prediction_value)

        if int(prediction_value) == 1:
            result = "High Risk"
        else:
            result = "Low Risk"

        chest_pain_labels = {
            "ATA": "Atypical Angina (ATA)",
            "NAP": "Non-Anginal Pain (NAP)",
            "ASY": "Asymptomatic (ASY)",
            "TA": "Typical Angina (TA)"
        }

        patient_input = {
            "Age": Age,
            "Sex": "Male" if Sex_original == "M" else "Female",
            "Chest Pain Type": chest_pain_labels[ChestPainType_original],
            "Resting Blood Pressure": f"{RestingBP} mmHg",
            "Cholesterol": f"{Cholesterol} mg/dL",
            "Fasting Blood Sugar": "Yes (> 120 mg/dL)" if FastingBS == 1 else "No (≤ 120 mg/dL)",
            "Resting ECG": RestingECG_original,
            "Maximum Heart Rate": f"{MaxHR} bpm",
            "Exercise Induced Angina": "Yes" if ExerciseAngina_original == "Y" else "No",
            "Oldpeak": Oldpeak,
            "ST Slope": ST_Slope_original
        }

        session["pending_prediction"] = {
            "Age": Age,
            "Sex": "Male" if Sex_original == "M" else "Female",
            "ChestPainType": chest_pain_labels[ChestPainType_original],
            "RestingBP": RestingBP,
            "Cholesterol": Cholesterol,
            "FastingBS": "Yes (> 120 mg/dL)" if FastingBS == 1 else "No (≤ 120 mg/dL)",
            "RestingECG": RestingECG_original,
            "MaxHR": MaxHR,
            "ExerciseAngina": "Yes" if ExerciseAngina_original == "Y" else "No",
            "Oldpeak": Oldpeak,
            "ST_Slope": ST_Slope_original,
            "result": result,
            "probability": round(confidence * 100, 2)
        }

        return render_template(
            "prediction.html",
            prediction=result,
            confidence=confidence,
            patient_input=patient_input
        )

    except Exception as e:
        print("PREDICTION ERROR:", str(e))
        return render_template(
            "prediction.html",
            error="Prediction failed: " + str(e)
        )


# ============================================================
# SAVE PREDICTION
# ============================================================
@app.route("/save-prediction", methods=["POST"])
def save_prediction():
    if not session.get("pending_prediction"):
        flash("No prediction available to save.", "error")
        return redirect(url_for("prediction_page"))

    if not current_user.is_authenticated:
        flash("Please login or register to save your prediction.", "info")
        return redirect(url_for("login"))

    return redirect(url_for("save_pending_prediction"))


# ============================================================
# SAVE PENDING PREDICTION TO DATABASE
# ============================================================
@app.route("/save-pending-prediction")
@login_required
def save_pending_prediction():
    pending = session.get("pending_prediction")

    if not pending:
        flash("No prediction found to save.", "error")
        return redirect(url_for("dashboard"))

    try:
        new_prediction = Prediction(
            user_id=current_user.id,
            age=pending["Age"],
            sex=pending["Sex"],
            chest_pain_type=pending["ChestPainType"],
            resting_bp=pending["RestingBP"],
            cholesterol=pending["Cholesterol"],
            fasting_bs=pending["FastingBS"],
            resting_ecg=pending["RestingECG"],
            max_hr=pending["MaxHR"],
            exercise_angina=pending["ExerciseAngina"],
            oldpeak=pending["Oldpeak"],
            st_slope=pending["ST_Slope"],
            result=pending["result"],
            probability=pending["probability"]
        )

        db.session.add(new_prediction)
        db.session.commit()
        session.pop("pending_prediction", None)
        flash("Prediction saved successfully!", "success")
        return redirect(url_for("dashboard"))

    except Exception as e:
        db.session.rollback()
        print("SAVE PREDICTION ERROR:", str(e))
        flash("Unable to save prediction: " + str(e), "error")
        return redirect(url_for("prediction_page"))


# ============================================================
# LOGOUT
# ============================================================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


# ============================================================
# RUN APPLICATION
# ============================================================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)