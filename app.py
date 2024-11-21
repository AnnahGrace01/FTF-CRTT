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
    "win_streak": 0,
    "loss_streak": 0,
    "last_winning_blasts": []  # Store player's blast levels when they win
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

    if player_won:
        # Update win streak and reset loss streak
        game_state["win_streak"] += 1
        game_state["loss_streak"] = 0

        # Update the list of last winning blasts
        game_state["last_winning_blasts"].append(player_blast)

        # Keep only the last three winning blasts
        if len(game_state["last_winning_blasts"]) > 3:
            game_state["last_winning_blasts"].pop(0)
    else:
        # Update loss streak and reset win streak
        game_state["loss_streak"] += 1
        game_state["win_streak"] = 0

    # Calculate velocity and acceleration based on last winning blasts
    last_blast = game_state["last_winning_blasts"][-1] if len(game_state["last_winning_blasts"]) >= 1 else 0
    velocity = (
        game_state["last_winning_blasts"][-1] - game_state["last_winning_blasts"][-2]
        if len(game_state["last_winning_blasts"]) >= 2 else 0
    )
    acceleration = (
        (game_state["last_winning_blasts"][-1] - game_state["last_winning_blasts"][-2])
        - (game_state["last_winning_blasts"][-2] - game_state["last_winning_blasts"][-3])
        if len(game_state["last_winning_blasts"]) >= 3 else 0
    )

    # Debug log: Updated game state
    print("Updated game state:", game_state)
    print(f"Last blast: {last_blast}, Velocity: {velocity}, Acceleration: {acceleration}")

    # If Bob needs to make a decision (when the player loses)
    if not player_won:
        input_data = pd.DataFrame({
            'velocity': [velocity],
            'acceleration': [acceleration],
            'win_streak': [game_state["win_streak"]],
            'loss_streak': [game_state["loss_streak"]],
            'opponent_last_sound': [last_blast],
            'opponent_velocity': [velocity],
            'opponent_acceleration': [acceleration]
        })

        # Debug log: Input to model
        print("Input data for bot model:", input_data)

        # Predict Bob's blast level
        bob_blast = bot_model.predict(input_data)[0]
        print("Bob's blast level:", bob_blast)  # Debug log

        return jsonify({'bob_blast': int(round(bob_blast))})

    return jsonify({})
