# ============================================================
# HEART DISEASE RISK PREDICTION SYSTEM
# FLASK BACKEND - OPTIMIZED FOR RENDER & PROFILE WHATSAPP RECOVERY
# ============================================================

from flask import (
    Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)
from flask_mail import Mail
import pandas as pd
import pickle
from pathlib import Path
import os
import secrets
import string
import urllib.parse
import urllib.request
import json
from datetime import datetime

# Import Authlib for Google Login and ProxyFix for Render Deployment
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix

# Import text for raw SQL execution
from sqlalchemy import text

from config import Config
from extensions import db, login_manager
from models import User, Prediction

# ============================================================
# CREATE FLASK APPLICATION
# ============================================================
app = Flask(__name__)

# Force Flask to respect Render's HTTPS routing headers
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

app.config.from_object(Config)

# FORCE HTTPS FOR URL GENERATION ON DEPLOYMENT
app.config['PREFERRED_URL_SCHEME'] = 'https'

# SESSION SECURITY
app.config['SECRET_KEY'] = app.config.get('SECRET_KEY')
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

# Google OAuth Credentials
app.config['GOOGLE_CLIENT_ID'] = "472208823648-hqal3kdqbbi8igap3trjvncqordu0vb0.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"

# ============================================================
# INITIALIZE EXTENSIONS & OAUTH
# ============================================================
db.init_app(app)
login_manager.init_app(app)
mail = Mail(app)

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


# ============================================================
# DIGITAL ASSET LINKS ROUTE (FOR GOOGLE PLAY DOMAIN VERIFICATION)
# ============================================================
@app.route('/.well-known/assetlinks.json')
def asset_links():
    return send_from_directory('static', 'assetlinks.json', mimetype='application/json')


# ============================================================
# SERVICE WORKER ROUTE (ROOT SCOPE FOR PWA CAPABILITIES)
# ============================================================
@app.route('/sw.js')
def service_worker():
    return send_from_directory('static/js', 'sw.js', mimetype='application/javascript')


# ============================================================
# CRASH-PROOF USER LOADER
# ============================================================
@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except Exception as e:
        print("Safely bypassing database schema error during user load.")
        return None


# ============================================================
# AUTOMATIC DATABASE PATCH (POSTGRESQL & MYSQL SAFE)
# ============================================================
with app.app_context():
    try:
        with db.engine.connect() as conn:
            # Patch is_disabled column
            try:
                conn.execute(text("ALTER TABLE users ADD COLUMN is_disabled BOOLEAN DEFAULT FALSE;"))
                conn.commit()
                print("Database patch: is_disabled column added!")
            except Exception:
                conn.rollback()

            # Patch phone column
            try:
                conn.execute(text("ALTER TABLE users ADD COLUMN phone VARCHAR(20);"))
                conn.commit()
                print("Database patch: phone column added!")
            except Exception:
                conn.rollback()
    except Exception as e:
        print("Database patch status check finished.")

    db.create_all()

    # Dispose startup connection pool to prevent stale/corrupted SSL sockets on Cloud DBs
    db.engine.dispose()

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


# ============================================================
# REGISTER (NO PHONE REQUIRED AT SIGNUP)
# ============================================================
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

        # Create user without phone (phone added later in Profile Settings)
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
# RESET PASSWORD VIA DIRECT ON-SCREEN / NEW TAB LINK
# ============================================================
@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()

        if not email:
            flash("Please enter a valid email address.", "error")
            return render_template("reset_request.html")

        user = User.query.filter_by(email=email).first()

        if user:
            token = user.get_reset_token()

            if 'onrender.com' in request.host or request.headers.get('X-Forwarded-Proto') == 'https':
                reset_url = url_for('reset_token', token=token, _external=True, _scheme='https')
            else:
                reset_url = url_for('reset_token', token=token, _external=True)

            return render_template(
                "reset_request.html",
                reset_url=reset_url,
                user_email=user.email,
                user_found=True
            )
        else:
            flash('That email address does not exist in our system.', 'error')

    return render_template("reset_request.html")


# ============================================================
# RESET PASSWORD VIA WHATSAPP (READS NUMBER FROM USER PROFILE)
# ============================================================
@app.route("/reset_whatsapp", methods=["GET", "POST"])
def reset_whatsapp():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip().lower()

        user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()

        if user:
            # Check if user has configured a contact number in profile settings
            if not user.phone or not str(user.phone).strip():
                flash('No contact number is configured in your profile settings. Please use Email Recovery.', 'error')
                return redirect(url_for('reset_whatsapp'))

            token = user.get_reset_token()

            if 'onrender.com' in request.host or request.headers.get('X-Forwarded-Proto') == 'https':
                reset_url = url_for('reset_token', token=token, _external=True, _scheme='https')
            else:
                reset_url = url_for('reset_token', token=token, _external=True)

            message_text = (
                f"Hello *{user.username}*,\n\n"
                f"Here is your secure password reset link for CardioPredict AI:\n\n"
                f"{reset_url}\n\n"
                f"This link expires in 30 minutes."
            )

            raw_phone = str(user.phone).strip()
            digits_only = "".join(filter(str.isdigit, raw_phone))

            if len(digits_only) == 10:
                formatted_phone = f"91{digits_only}"
            else:
                formatted_phone = digits_only

            if not formatted_phone:
                flash('Registered contact number in your profile is invalid. Please update it or use Email Recovery.', 'error')
                return redirect(url_for('reset_whatsapp'))

            INSTANCE_ID = "instance187614"
            TOKEN = "2wvg9k0bomw8nvqj"
            api_url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"

            try:
                post_data = urllib.parse.urlencode({
                    "token": TOKEN,
                    "to": formatted_phone,
                    "body": message_text,
                    "priority": "10"
                }).encode('utf-8')

                req = urllib.request.Request(
                    api_url,
                    data=post_data,
                    headers={
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'User-Agent': 'Mozilla/5.0'
                    }
                )

                with urllib.request.urlopen(req) as response:
                    res = json.loads(response.read().decode('utf-8'))

                if res.get("sent") == "true" or res.get("sent") is True or res.get("id"):
                    flash('Password reset link sent directly to your registered WhatsApp number!', 'success')
                    return render_template("reset_whatsapp_success.html")
                else:
                    error_msg = res.get("error") or res.get("message") or "Failed to send message via UltraMsg."
                    print(f"UltraMsg API Error Response: {res}")
                    flash(f'WhatsApp API Error: {error_msg}', 'error')
                    return redirect(url_for('reset_whatsapp'))

            except Exception as e:
                print(f"UltraMsg API Dispatch Exception: {str(e)}")
                flash('Server error while dispatching WhatsApp message.', 'error')
                return redirect(url_for('reset_whatsapp'))
        else:
            flash('No account found with that email address or username.', 'error')

    return render_template("reset_whatsapp.html")


# ============================================================
# VERIFY TOKEN & CHANGE PASSWORD ROUTE
# ============================================================
@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token.', 'error')
        return redirect(url_for('reset_request'))

    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_token.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('reset_token.html')

        user.set_password(password)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template("reset_token.html")


# ============================================================
# GOOGLE OAUTH LOGIN ROUTES
# ============================================================
@app.route('/login/google')
def google_login():
    session['google_action'] = request.args.get('action', 'login')

    if 'onrender.com' in request.host or request.headers.get('X-Forwarded-Proto') == 'https':
        redirect_uri = url_for('google_authorize', _external=True, _scheme='https')
    else:
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

        action = session.get('google_action', 'login')

        if not user:
            if action == 'login':
                flash("Account does not exist. Please register first.", "error")
                return redirect(url_for('login'))
            else:
                session['google_email'] = email
                session['google_name'] = name
                return redirect(url_for('google_setup'))

        if action == 'register':
            flash("Account already exists. Please login instead.", "error")
            return redirect(url_for('login'))
        else:
            flash(f"Welcome back, {user.username}!", "success")

        login_user(user, remember=True)

        if session.get("pending_prediction"):
            return redirect(url_for("save_pending_prediction"))

        return redirect(url_for('dashboard'))

    except Exception as e:
        flash(f"Authentication failed: {str(e)}", "error")
        return redirect(url_for('login'))


# ============================================================
# GOOGLE ACCOUNT SETUP
# ============================================================
@app.route('/google-setup', methods=['GET', 'POST'])
def google_setup():
    if 'google_email' not in session:
        return redirect(url_for('register'))

    email = session.get('google_email')
    name = session.get('google_name')

    if name:
        suggested_username = name.replace(" ", "")
    else:
        suggested_username = email.split("@")[0] if email else "User"

    if request.method == 'POST':
        username = request.form.get('username').strip()

        if not username:
            return render_template('google_setup.html', email=email, suggested_username=suggested_username,
                                   error="Username is required.")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('google_setup.html', email=email, suggested_username=username,
                                   error="Username is already taken. Please choose another.")

        alphabet = string.ascii_letters + string.digits + string.punctuation
        random_password = ''.join(secrets.choice(alphabet) for i in range(20))

        new_user = User(username=username, email=email)
        new_user.set_password(random_password)

        db.session.add(new_user)
        db.session.commit()

        session.pop('google_email', None)
        session.pop('google_name', None)

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
    if current_user.is_disabled:
        predictions = []
    else:
        predictions = Prediction.query.filter_by(
            user_id=current_user.id
        ).order_by(Prediction.created_at.desc()).all()

    return render_template("dashboard.html", predictions=predictions)


# ============================================================
# UPDATE PROFILE (SAVES WHATSAPP CONTACT NUMBER)
# ============================================================
@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()
    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    user = db.session.get(User, current_user.id)

    try:
        # Check current password before committing any profile updates
        if not current_password:
            flash("Please enter your current password to save profile changes.", "error")
            return redirect(url_for("dashboard"))

        if not user.check_password(current_password):
            flash("Incorrect current password.", "error")
            return redirect(url_for("dashboard"))

        if username and username != user.username:
            if User.query.filter_by(username=username).first():
                flash("Username is already taken.", "error")
                return redirect(url_for("dashboard"))
            user.username = username

        if email and email != user.email:
            if User.query.filter_by(email=email).first():
                flash("Email is already registered.", "error")
                return redirect(url_for("dashboard"))
            user.email = email

        # Update WhatsApp Contact Number
        user.phone = phone

        if new_password or confirm_password:
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
# DISABLE ACCOUNT
# ============================================================
@app.route("/disable_account", methods=["POST"])
@login_required
def disable_account():
    user = db.session.get(User, current_user.id)
    user.is_disabled = True
    db.session.commit()
    flash("Your account has been disabled. Your results are now hidden.", "info")
    return redirect(url_for("dashboard"))


# ============================================================
# ENABLE ACCOUNT
# ============================================================
@app.route("/enable_account", methods=["POST"])
@login_required
def enable_account():
    user = db.session.get(User, current_user.id)
    user.is_disabled = False
    db.session.commit()
    flash("Account restored! Your data is visible again.", "success")
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
    if current_user.is_disabled:
        flash("You cannot view reports while your account is disabled.", "error")
        return redirect(url_for("dashboard"))

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

        # Categorize into 3 risk tiers based on probability percentage
        probability_pct = confidence * 100

        if probability_pct >= 70.0:
            result = "High Risk"
        elif probability_pct >= 30.0:
            result = "Medium Risk"
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
            "Fasting BS": "Yes (> 120 mg/dL)" if FastingBS == 1 else "No (≤ 120 mg/dL)",
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
            "probability": round(probability_pct, 2),
            "created_at": datetime.now().isoformat()
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
    if current_user.is_disabled:
        flash("You cannot save predictions while your account is disabled.", "error")
        return redirect(url_for("dashboard"))

    pending = session.get("pending_prediction")

    if not pending:
        flash("No prediction found to save.", "error")
        return redirect(url_for("dashboard"))

    try:
        prediction_time = datetime.fromisoformat(pending["created_at"]) if "created_at" in pending else datetime.now()

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
            probability=pending["probability"],
            created_at=prediction_time
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