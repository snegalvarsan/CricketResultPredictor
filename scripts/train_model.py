import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("data/match_data.csv")

# Drop rows with missing target
df = df[df["match_winner"].notna()]

# Define features and target
features = ["team1", "team2", "venue", "toss_winner", "toss_decision"]
X = pd.get_dummies(df[features])
y = df["match_winner"]

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"✅ Model trained with accuracy: {accuracy:.2f}")

# Save model
os.makedirs("models", exist_ok=True)
with open("models/win_predictor.pkl", "wb") as f:
    pickle.dump(model, f)
print("📦 Model saved to models/win_predictor.pkl")
