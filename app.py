import os
import pandas as pd
import joblib
from flask import Flask, request, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)

# Load the bot model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "bot_model.pkl")
bot_model = joblib.load(MODEL_PATH)

# Initialize game state
game_state = {
    "round": 1,
    "game_data": {},  # Store all round data
    "win_streak": 0,
    "loss_streak": 0,
}

@app.route("/")
def home():
    return render_template("index.html")  # Serve the HTML frontend

@app.route("/play_round", methods=["POST"])
def play_round():
    data = request.json
    player_blast = data.get("player_blast", 0)  # Player's current blast level
    round_num = game_state["round"]

    # Calculate previous data if applicable
    if round_num == 1:
        velocity = 0
        acceleration = 0
        opponent_last_sound = 0
        opponent_velocity = 0
        opponent_acceleration = 0
    else:
        game_data = game_state["game_data"]
        opponent_last_sound = int(game_data.get(round_num - 1, {}).get("blast_level", 0))

        # Bob's velocity and acceleration
        if round_num > 2:
            last_blast = int(game_data.get(round_num - 1, {}).get("blast_level", 0))
            prev_blast = int(game_data.get(round_num - 2, {}).get("blast_level", 0))
            velocity = last_blast - prev_blast
            if round_num > 3:
                prev_prev_blast = int(game_data.get(round_num - 3, {}).get("blast_level", 0))
                acceleration = velocity - (prev_blast - prev_prev_blast)
            else:
                acceleration = 0
        else:
            velocity = 0
            acceleration = 0

        # Player's velocity and acceleration
        if round_num > 2:
            opponent_last_sound_2 = int(game_data.get(round_num - 2, {}).get("blast_level", 0))
            opponent_velocity = opponent_last_sound - opponent_last_sound_2
            if round_num > 3:
                opponent_acceleration = opponent_velocity - (opponent_last_sound_2 - int(game_data.get(round_num - 3, {}).get("blast_level", 0)))
            else:
                opponent_acceleration = 0
        else:
            opponent_velocity = 0
            opponent_acceleration = 0

    # Calculate win/loss streaks
    if data.get("player_won", False):
        game_state["win_streak"] += 1
        game_state["loss_streak"] = 0
    else:
        game_state["win_streak"] = 0
        game_state["loss_streak"] += 1

    # Prepare input data for Bob's decision
    input_data = pd.DataFrame({
        "velocity": [velocity],
        "acceleration": [acceleration],
        "win_streak": [game_state["win_streak"]],
        "loss_streak": [game_state["loss_streak"]],
        "opponent_last_sound": [opponent_last_sound],
        "opponent_velocity": [opponent_velocity],
        "opponent_acceleration": [opponent_acceleration],
    })

    bob_blast = int(round(bot_model.predict(input_data)[0]))
    game_state["game_data"][round_num] = {"blast_level": bob_blast}

    # Increment the round number
    game_state["round"] += 1

    return jsonify({
        "bob_blast": bob_blast,
        "win_streak": game_state["win_streak"],
        "loss_streak": game_state["loss_streak"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
