import pickle
import sklearn
print(f"sklearn version: {sklearn.__version__}")
try:
    heart_model = pickle.load(open('Saved_Models/heart_disease_model.sav', 'rb'))
    print("Heart model loaded successfully.")
    diabetes_model = pickle.load(open('Saved_Models/diabetes_model.sav', 'rb'))
    print("Diabetes model loaded successfully.")
    parkinsons_model = pickle.load(open('Saved_Models/parkinsons_model.sav', 'rb'))
    print("Parkinsons model loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")
