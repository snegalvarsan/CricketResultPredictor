import streamlit as st
import pandas as pd
import pickle
import os

st.set_page_config(page_title="Cricket Match Predictor", layout="wide")

st.title("🏏 Cricket Match Predictor")
st.markdown("Predict match outcome based on historical data")

# Load model
MODEL_PATH = "models/win_predictor.pkl"
if os.path.exists(MODEL_PATH):
    model = pickle.load(open(MODEL_PATH, 'rb'))
else:
    st.error("⚠️ ML model not found. Please train the model first.")
    st.stop()

# Load venues, teams
df = pd.read_csv("data/match_data.csv")
teams = sorted(set(df['team1']).union(set(df['team2'])))
venues = sorted(df['venue'].dropna().unique())

# Sidebar inputs
st.sidebar.header("Input Match Details")
team1 = st.sidebar.selectbox("Select Team 1", teams)
team2 = st.sidebar.selectbox("Select Team 2", [t for t in teams if t != team1])
venue = st.sidebar.selectbox("Select Venue", venues)
toss_winner = st.sidebar.selectbox("Toss Winner", [team1, team2])
toss_decision = st.sidebar.selectbox("Toss Decision", ["bat", "field"])

if st.sidebar.button("Predict Winner"):
    input_df = pd.DataFrame([{
        "team1": team1,
        "team2": team2,
        "venue": venue,
        "toss_winner": toss_winner,
        "toss_decision": toss_decision
    }])

    # Encoding same as training
    X = pd.get_dummies(input_df)
    model_cols = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else X.columns
    for col in model_cols:
        if col not in X:
            X[col] = 0
    X = X[model_cols]

    # Prediction
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X)[0]

    st.success(f"🏆 Predicted Winner: **{prediction}**")
    percent = round(max(proba) * 100, 2)
    st.write(f" Win Possibility Prediction: {percent}%")
