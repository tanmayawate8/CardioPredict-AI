# ❤️ Heart Disease Risk Prediction

## 📌 Project Overview

Heart Disease Risk Prediction is a Machine Learning-based web application that predicts whether a patient is at risk of heart disease using medical parameters. The project applies data preprocessing, exploratory data analysis, machine learning model development, hyperparameter tuning, model evaluation, and deployment using Flask.

The system provides users with a simple web interface where patient information can be entered to receive an instant prediction.

---

# 🎯 Objectives

- Predict heart disease risk using Machine Learning.
- Compare multiple machine learning algorithms.
- Improve model performance using Hyperparameter Tuning.
- Deploy the best-performing model using Flask.
- Provide a user-friendly web interface for prediction.

---

# 🚀 Features

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Data Preprocessing
- Train-Test Splitting
- Multiple Machine Learning Models
- Hyperparameter Tuning
- Model Evaluation
- Best Model Selection
- Model Serialization
- Prediction Pipeline Testing
- Flask Web Application
- Responsive HTML/CSS/JavaScript Interface

---

# 🧠 Machine Learning Models

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost

---

# 🛠 Technologies Used

## Programming Language

- Python

## Machine Learning

- Scikit-learn
- XGBoost

## Data Analysis

- Pandas
- NumPy

## Data Visualization

- Matplotlib
- Seaborn

## Backend

- Flask

## Frontend

- HTML5
- CSS3
- JavaScript

## Model Storage

- Pickle

---

# 📂 Project Structure

```
Heart Disease Risk Prediction
│
├── Dataset
│   ├── heart.csv
│   ├── cleaned_heart_data.csv
│   ├── preprocessed_heart_data.csv
│   ├── X_train.csv
│   ├── X_test.csv
│   ├── y_train.csv
│   └── y_test.csv
│
├── Phase 1 - Problem Definition
│
├── Phase 2 - Dataset Collection & Understanding
│
├── Phase 3 - Data Loading
│
├── Phase 4 - Data Cleaning
│
├── Phase 5 - Exploratory Data Analysis
│
├── Phase 6 - Data Preprocessing
│
├── Phase 7 - Train Test Splitting
│
├── Phase 8 - Model Development
│   ├── Logistic Regression
│   ├── Decision Tree
│   ├── Random Forest
│   └── XGBoost
│
├── Phase 9 - Model Evaluation
│
├── Phase 10 - Best Model Selection
│
├── Phase 11 - Model Serialization
│
├── Phase 12 - Prediction Pipeline Testing
│
├── Hyper Parameter Tuning
│
├── WebApp
│   ├── app.py
│   ├── heart_disease_model.pkl
│   ├── templates
│   └── static
│
└── README.md
```

---

# 📊 Dataset Information

The project uses the Heart Disease Prediction dataset containing patient medical records.

### Features

- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate
- Exercise-Induced Angina
- Oldpeak
- ST Slope

### Target Variable

- HeartDisease
  - 0 → No Heart Disease
  - 1 → Heart Disease

---

# ⚙ Project Workflow

1. Problem Definition
2. Dataset Collection
3. Data Loading
4. Data Cleaning
5. Exploratory Data Analysis
6. Data Preprocessing
7. Train-Test Split
8. Model Development
9. Model Evaluation
10. Best Model Selection
11. Hyperparameter Tuning
12. Model Serialization
13. Prediction Pipeline Testing
14. Flask Web Deployment

---

# 📈 Model Performance

| Model | Accuracy |
|--------|----------|
| Logistic Regression | 86.41% |
| Decision Tree | 84.24% |
| Random Forest | 89.67% |
| XGBoost | 91.85% |

---

# 🏆 Best Model

**XGBoost Classifier**

Performance:

- Accuracy: 91.85%
- Precision: 92.60%
- Recall: 91.50%
- F1-Score: 92.00%

The XGBoost model achieved the highest prediction accuracy and was selected as the final deployment model.

---

# 🌐 Web Application

The Flask application allows users to:

- Enter patient medical information
- Predict heart disease risk
- Display prediction confidence
- View responsive user interface
- Access About and Contact pages

---

# ▶️ Installation

Clone the repository

```bash
git clone https://github.com/tanmayawate8/Heart-Disease-risk-prediction.git
```

Move to the project directory

```bash
cd Heart-Disease-risk-prediction
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

# 📦 Required Libraries

```text
Flask
Pandas
NumPy
Scikit-learn
Matplotlib
Seaborn
XGBoost
Pickle
```

Install all libraries

```bash
pip install flask pandas numpy matplotlib seaborn scikit-learn xgboost
```

---

# 💡 Future Improvements

- Deep Learning Model
- Feature Selection
- Cloud Deployment
- User Authentication
- Database Integration
- Doctor Recommendation System
- PDF Report Generation
- API Integration
- Mobile Application

---

# 📚 Learning Outcomes

This project demonstrates practical implementation of:

- Data Cleaning
- Exploratory Data Analysis
- Feature Engineering
- Data Preprocessing
- Machine Learning Algorithms
- Hyperparameter Tuning
- Model Evaluation
- Model Deployment
- Flask Web Development
- Git & GitHub Version Control

---

# 👨‍💻 Author

**Tanmay Awate**

Diploma in Computer Engineering

GitHub:
https://github.com/tanmayawate8

LinkedIn:
(Add your LinkedIn profile)

---

# 📄 License

This project is developed for educational and research purposes.

---

⭐ If you found this project helpful, consider giving it a Star on GitHub!
