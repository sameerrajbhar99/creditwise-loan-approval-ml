import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib
import os

def generate_synthetic_data(n=1000):
    np.random.seed(42)
    data = {
        'Applicant_Income': np.random.randint(2000, 20000, n),
        'Coapplicant_Income': np.random.randint(0, 10000, n),
        'Age': np.random.randint(21, 65, n),
        'Dependents': np.random.randint(0, 5, n),
        'Credit_Score': np.random.randint(300, 850, n),
        'Existing_Loans': np.random.randint(0, 5, n),
        'DTI_Ratio': np.random.uniform(0.1, 0.8, n),
        'Savings': np.random.randint(0, 50000, n),
        'Collateral_Value': np.random.randint(0, 100000, n),
        'Loan_Amount': np.random.randint(5000, 50000, n),
        'Loan_Term': np.random.choice([12, 24, 36, 48, 60, 72, 84, 120, 360], n),
        'Loan_Purpose': np.random.choice(['Personal', 'Home', 'Education', 'Car'], n),
        'Property_Area': np.random.choice(['Urban', 'Semiurban', 'Rural'], n),
        'Gender': np.random.choice(['Male', 'Female'], n),
        'Employer_Category': np.random.choice(['Private', 'Government', 'MNC', 'Unemployed'], n),
        'Employment_Status': np.random.choice(['Salaried', 'Self-employed', 'Unemployed'], n),
        'Marital_Status': np.random.choice(['Married', 'Single'], n),
        'Education_Level': np.random.choice(['Graduate', 'Not Graduate'], n)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate some realistic target logic
    score = (
        (df['Credit_Score'] > 600).astype(int) * 3 +
        (df['Applicant_Income'] > 5000).astype(int) * 2 +
        (df['DTI_Ratio'] < 0.4).astype(int) * 2 +
        (df['Savings'] > 10000).astype(int) * 1 +
        (df['Existing_Loans'] < 2).astype(int) * 1 -
        (df['Employment_Status'] == 'Unemployed').astype(int) * 3
    )
    
    # Add some noise
    score = score + np.random.normal(0, 1, n)
    
    df['Loan_Approved'] = (score > 5).astype(int)
    
    return df

def preprocess_and_train(df):
    # Match the notebook logic
    df['DTI_Ratio_sq'] = df['DTI_Ratio'] ** 2
    df['Credit_Score_sq'] = df['Credit_Score'] ** 2
    
    y = df['Loan_Approved']
    X = df.drop(columns=['Loan_Approved', 'Credit_Score', 'DTI_Ratio'])
    
    # Encode categoricals
    cat_cols = X.select_dtypes(include=['object']).columns
    X = pd.get_dummies(X, columns=cat_cols, drop_first=True)
    
    # Save the feature columns so the web app knows the exact shape
    feature_columns = X.columns.tolist()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    train_acc = model.score(X_train_scaled, y_train)
    test_acc = model.score(scaler.transform(X_test), y_test)
    print(f"Model trained! Train Acc: {train_acc:.3f}, Test Acc: {test_acc:.3f}")
    
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/model.joblib')
    joblib.dump(scaler, 'model/scaler.joblib')
    joblib.dump(feature_columns, 'model/features.joblib')
    
    print("Model, scaler, and features saved to 'model/' directory.")

if __name__ == '__main__':
    print("Generating synthetic data...")
    df = generate_synthetic_data(2000)
    print("Training model...")
    preprocess_and_train(df)
