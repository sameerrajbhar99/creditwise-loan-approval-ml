# CreditWise: Loan Approval Prediction using Machine Learning

## Project Overview
CreditWise is an end-to-end supervised Machine Learning project designed to predict loan approval status based on applicant financial and credit-related information.

The system classifies whether a loan should be approved or rejected using multiple ML models and performance comparison. **This repository now includes a fully functional, stunning web application** that serves the best-performing model (Logistic Regression) via a Flask API.

---

## Web Application Features
- **Modern UI**: Stunning, premium dark-themed interface with glassmorphism effects.
- **Interactive Multi-Step Form**: Clean user experience broken down into Personal, Financial, and Loan details.
- **Real-Time Predictions**: The Flask backend runs the trained ML model pipeline to process input and provide immediate predictions.
- **Probability Gauge**: Visualizes the approval chance directly in the UI.

## Tech Stack
- **Backend**: Python, Flask, Pandas, Scikit-learn, Joblib
- **Frontend**: HTML5, CSS3 (Vanilla, Variables, Glassmorphism), Vanilla JavaScript
- **ML Models**: K-Nearest Neighbors (KNN), Logistic Regression, Naive Bayes

---

## Running the Web App Locally

1. **Install Dependencies**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Data & Train Model**
   Since the original dataset contains private information, run the training script to generate a synthetic dataset and train the Logistic Regression model:
   ```bash
   python generate_data_and_train.py
   ```
   This will create a `model/` directory containing the trained model and scaler.

3. **Start the Flask Server**
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000/`.

---

## Deployment to Cloud
This application is ready to be deployed to platforms like **Render**, **Heroku**, or **Railway**.
A `Procfile` is included for immediate compatibility with standard Python hosting environments.

- **Heroku / Render setup**: 
  - Ensure the `model/` directory is generated before pushing (or run the training script as part of the build step).
  - The `Procfile` correctly points to `web: gunicorn app:app`.

---

## Problem Statement
Financial institutions need an efficient way to evaluate loan applications and minimize risk.  
This project builds a classification model to automate loan approval decisions based on applicant data.

---

## Exploratory Data Analysis (EDA) & Feature Engineering
- Checked missing values and analyzed feature distributions.
- Feature scaling, one-hot encoding of categorical variables.
- Engineered features such as Debt-to-Income (DTI) ratio squared.

## Models Implemented & Evaluated
- K-Nearest Neighbors (KNN)
- Logistic Regression (Selected for production: ~87% Accuracy)
- Naive Bayes

## Key Learnings
- Building an end-to-end ML pipeline
- Model comparison strategies
- Designing an API and stunning frontend for ML inference
- Real-world financial risk modeling concepts
