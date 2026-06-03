from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import numpy as np
import joblib
import os

app = Flask(__name__, static_folder='static')

# Load models and features
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
try:
    model = joblib.load(os.path.join(MODEL_DIR, 'model.joblib'))
    scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.joblib'))
    feature_columns = joblib.load(os.path.join(MODEL_DIR, 'features.joblib'))
except Exception as e:
    print("Model files not found. Run generate_data_and_train.py first.")
    model, scaler, feature_columns = None, None, None

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not trained'}), 500
        
    try:
        data = request.json
        # Create DataFrame from input
        df = pd.DataFrame([data])
        
        # Numeric conversions
        num_cols = ['Applicant_Income', 'Coapplicant_Income', 'Age', 'Dependents', 
                   'Credit_Score', 'Existing_Loans', 'DTI_Ratio', 'Savings', 
                   'Collateral_Value', 'Loan_Amount', 'Loan_Term']
        
        for col in num_cols:
            df[col] = pd.to_numeric(df.get(col, 0), errors='coerce').fillna(0)
            
        # Feature Engineering as in notebook
        df['DTI_Ratio_sq'] = df['DTI_Ratio'] ** 2
        df['Credit_Score_sq'] = df['Credit_Score'] ** 2
        
        # Drop original columns (like notebook did)
        df = df.drop(columns=['Credit_Score', 'DTI_Ratio'])
        
        # Get dummies
        cat_cols = ['Loan_Purpose', 'Property_Area', 'Gender', 'Employer_Category', 
                   'Employment_Status', 'Marital_Status', 'Education_Level']
        df = pd.get_dummies(df, columns=cat_cols)
        
        # Ensure all columns from training are present
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0
                
        # Reorder columns to match training exactly
        X = df[feature_columns]
        
        # Scale and predict
        X_scaled = scaler.transform(X)
        prob = model.predict_proba(X_scaled)[0][1]
        prediction = bool(prob > 0.5)
        
        return jsonify({
            'approved': prediction,
            'probability': float(prob)
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
