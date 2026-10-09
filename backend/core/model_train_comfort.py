import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import joblib
import os

# 1. Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'processed_study_comfort_data.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'backend', 'models')

# 2. Load the preprocessed dataset
print("Loading data...")
df = pd.read_csv(DATA_PATH)

# 3. Define Features (X) and Target (y) for the Comfort Score
features = ['temperature', 'humidity', 'noise', 'CO2', 'ASR', 'elapsed_time_min', 'peopleCount']
X = df[features]
y = df['Comfort_Score']

# 4. Train/Test Split to verify accuracy before saving
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

print("Training Random Forest Regressor for Comfort Score...")
rf_regressor = RandomForestRegressor(random_state=42, n_estimators=100)
rf_regressor.fit(X_train, y_train)

# 5. Evaluate the Model (Check accuracy)
predictions = rf_regressor.predict(X_test)
r2 = r2_score(y_test, predictions)
print(f"Model R2 Score (Accuracy): {r2:.4f}")

# 6. Retrain on the full dataset and Save
rf_regressor.fit(X, y)
model_filename = os.path.join(MODEL_DIR, 'rf_comfort_model.pkl')
joblib.dump(rf_regressor, model_filename)

print(f"Success! Comfort Model permanently saved to: {model_filename}")