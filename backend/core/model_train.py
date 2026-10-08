import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# 1. Dynamically define paths so this works on any group member's computer
# This finds the root 'ComfortSense-Analytics' folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'processed_study_comfort_data.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'backend', 'models')

# Create the models folder if it doesn't exist
os.makedirs(MODEL_DIR, exist_ok=True)

print(f"Looking for data at: {DATA_PATH}")

# 2. Load the preprocessed dataset
df = pd.read_csv(DATA_PATH)

# 3. Define Features (X) and Target (y)
features = ['temperature', 'humidity', 'noise', 'CO2', 'ASR', 'elapsed_time_min', 'peopleCount']
X = df[features]
y = df['Attention_Level']

# 4. Initialize and Train the Random Forest Model
# We train on the entire dataset here because we already validated its accuracy during the Colab phase
print("Training Random Forest model...")
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X, y)

# 5. Export and Save the Model
model_filename = os.path.join(MODEL_DIR, 'rf_attention_model.pkl')
joblib.dump(rf_model, model_filename)

print(f"Success! Model permanently saved to: {model_filename}")