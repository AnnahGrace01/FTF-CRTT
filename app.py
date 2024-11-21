import os
import random
import time
import pandas as pd
import numpy as np
import joblib
from flask import Flask, request, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)

# Load the bot model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "bot_model.pkl")
bot_model = joblib.load(MODEL_PATH)

# Main page route
@app.route('/')
def home():
    return render_template('index.html')  # Simple HTML front-end for the game

# API route to handle bot's decision-making
@app.route('/bot_decision', methods=['POST'])
def bot_decision():
    data = request.json
    velocity = data.get('velocity', 0)
    acceleration = data.get('acceleration', 0)
    win_streak = data.get('win_streak', 0)
    loss_streak = data.get('loss_streak', 0)
    opponent_last_sound = data.get('opponent_last_sound', 0)
    opponent_velocity = data.get('opponent_velocity', 0)
    opponent_acceleration = data.get('opponent_acceleration', 0)

    # Prepare input data for the bot model
    input_data = pd.DataFrame([[velocity, acceleration, win_streak, loss_streak,
                                opponent_last_sound, opponent_velocity, opponent_acceleration]],
                              columns=['velocity', 'acceleration', 'win_streak', 'loss_streak',
                                       'opponent_last_sound', 'opponent_velocity', 'opponent_acceleration'])

    # Predict bot's blast level
    predicted_blast = bot_model.predict(input_data)[0]
    return jsonify({'bot_blast': int(round(predicted_blast))})

# Debugging endpoint to verify the server is running
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Running!'})

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
