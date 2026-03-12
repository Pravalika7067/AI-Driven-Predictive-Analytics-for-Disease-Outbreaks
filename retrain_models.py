import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import pickle
import os

# Create Saved_Models directory if it doesn't exist
os.makedirs('Saved_Models', exist_ok=True)

def train_heart():
    print("Training Heart Disease Model...")
    data = pd.read_csv('Datasets/heart.csv')
    X = data.drop(columns='target', axis=1)
    Y = data['target']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=10)
    model.fit(X_scaled, Y)
    
    with open('Saved_Models/heart_disease_model.sav', 'wb') as f:
        pickle.dump(model, f)
    with open('Saved_Models/scaler_heart.sav', 'wb') as f:
        pickle.dump(scaler, f)
    print("Heart model and scaler saved.")

def train_diabetes():
    print("Training Diabetes Model...")
    data = pd.read_csv('Datasets/diabetes.csv')
    X = data.drop(columns='Outcome', axis=1)
    Y = data['Outcome']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Note: Diabetes notebook used random_state=2
    model = RandomForestClassifier(random_state=2, n_estimators=100, max_depth=10)
    model.fit(X_scaled, Y)
    
    with open('Saved_Models/diabetes_model.sav', 'wb') as f:
        pickle.dump(model, f)
    with open('Saved_Models/scaler_diabetes.sav', 'wb') as f:
        pickle.dump(scaler, f)
    print("Diabetes model and scaler saved.")

def train_parkinsons():
    print("Training Parkinson's Model...")
    data = pd.read_csv('Datasets/parkinsons.csv')
    X = data.drop(columns=['name', 'status'], axis=1)
    Y = data['status']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Parkinson notebook used svm.SVC
    model = svm.SVC(random_state=2, probability=True)
    model.fit(X_scaled, Y)
    
    with open('Saved_Models/parkinsons_model.sav', 'wb') as f:
        pickle.dump(model, f)
    with open('Saved_Models/scaler_parkinsons.sav', 'wb') as f:
        pickle.dump(scaler, f)
    print("Parkinson's model and scaler saved.")

if __name__ == "__main__":
    train_heart()
    train_diabetes()
    train_parkinsons()
