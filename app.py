import os
import pandas as pd
import joblib
from flask import Flask, request, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)

# Load the bot model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "bot_model.pkl")
bot_model = joblib.load(MODEL_PATH)

# Game state variables (persistent across rounds)
game_state = {
    "velocity": 0,
    "acceleration": 0,
    "win_streak": 0,
    "loss_streak": 0,
    "opponent_last_sound": 0,
    "opponent_velocity": 0,
    "opponent_acceleration": 0
}

# Main page route
@app.route('/')
def home():
    return render_template('index.html')

# Play round route
@app.route('/play_round', methods=['POST'])
def play_round():
    global game_state

    # Receive data from the frontend
    data = request.json
    player_blast = int(data.get('player_blast', 0))
    player_won = data.get('player_won', False)

    # Debug log: Player data
    print("Received data from player:", data)

    # Update win/loss streaks
    if player_won:
        game_state["win_streak"] += 1
        game_state["loss_streak"] = 0
    else:
        game_state["win_streak"] = 0
        game_state["loss_streak"] += 1

    # Update velocity and acceleration
    opponent_velocity = player_blast - game_state["opponent_last_sound"]
    opponent_acceleration = opponent_velocity - game_state["velocity"]
    game_state["velocity"] = opponent_velocity
    game_state["acceleration"] = opponent_acceleration
    game_state["opponent_last_sound"] = player_blast

    # Debug log: Updated game state
    print("Updated game state:", game_state)

    # If Bob needs to make a decision
    if not player_won:
        input_data = pd.DataFrame({
            'velocity': [game_state["velocity"]],
            'acceleration': [game_state["acceleration"]],
            'win_streak': [game_state["win_streak"]],
            'loss_streak': [game_state["loss_streak"]],
            'opponent_last_sound': [game_state["opponent_last_sound"]],
            'opponent_velocity': [game_state["opponent_velocity"]],
            'opponent_acceleration': [game_state["opponent_acceleration"]]
        })

        # Debug log: Input to model
        print("Input data for bot model:", input_data)

        # Predict Bob's blast level
        bob_blast = bot_model.predict(input_data)[0]
        print("Bob's blast level:", bob_blast)  # Debug log

        return jsonify({'bob_blast': int(round(bob_blast))})

    return jsonify({})
