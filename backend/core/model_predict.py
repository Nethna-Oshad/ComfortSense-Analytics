import os
import joblib
import pandas as pd

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'rf_attention_model.pkl')

# Load the model into memory when the API starts
if os.path.exists(MODEL_PATH):
    rf_model = joblib.load(MODEL_PATH)
else:
    rf_model = None

def generate_predictions(feature_vector: pd.DataFrame):
    """
    Passes the fused feature vector to the Random Forest model.
    """
    if rf_model is None:
        return {"error": "Model file not found. Train the model first."}
    
    # Predict Attention Level
    attention_pred = rf_model.predict(feature_vector)[0]
    
    # Calculate an estimated Comfort Score (Mock calculation based on CO2/Temp for API demo)
    co2_val = feature_vector['CO2'].values[0]
    if co2_val >= 1000:
        comfort_score = 25.0
    elif co2_val >= 800:
        comfort_score = 50.0
    else:
        comfort_score = 85.0
        
    return {
        "Attention_Level": attention_pred,
        "Comfort_Score": comfort_score,
        "Actionable_Recommendation": "Increase ventilation" if attention_pred == "Low" else "Optimal conditions"
    }