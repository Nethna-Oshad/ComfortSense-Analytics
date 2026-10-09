import sys
import os
import datetime
from fastapi.testclient import TestClient

# Force Pytest to recognize the current backend directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

# Create a test client that bypasses the need for a live server
client = TestClient(app)

def test_root_endpoint():
    """Verifies the API is online."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ComfortSense Predictive Engine is online."}

def test_predict_endpoint():
    """Verifies the ML models process data and return the correct dictionary structure."""
    payload = {
        "room_id": "Test Lab",
        "session_start_time": datetime.datetime.now().isoformat(),
        "readings": [
            {
                "timestamp": datetime.datetime.now().isoformat(),
                "temperature": 24.5,
                "humidity": 55.0,
                "noise": 40.0,
                "CO2": 850.0,
                "peopleCount": 25
            }
        ]
    }
    
    response = client.post("/api/predict", json=payload)
    
    # Prove the server accepted the request (Status 200)
    assert response.status_code == 200
    
    data = response.json()
    predictions = data["predictions"]
    
    # Prove the machine learning models returned the required outputs
    assert "Comfort_Score" in predictions
    assert "Attention_Level" in predictions
    assert "Actionable_Recommendation" in predictions
    
    # Prove the Comfort Score is a valid percentage
    assert 0.0 <= predictions["Comfort_Score"] <= 100.0