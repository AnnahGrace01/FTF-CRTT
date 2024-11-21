from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained bot model
bot_model = joblib.load('bot_model.pkl')

# Game state variables
game_state = {
    "player_last_wins": [],  # Tracks player's last winning blast levels
    "player_last_level": 0,
    "player_velocity": 0,
    "player_acceleration": 0,
    "win_streak": 0,
    "loss_streak": 0,
    "waiting_for_blast": False,  # Track if waiting for player to select a blast
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/play_round', methods=['POST'])
def play_round():
    data = request.json

    # Extract player data
    player_blast = data.get('player_blast', 0)
    player_won = data.get('player_won', False)

    if player_won:
        # Update player stats on a win
        game_state["player_last_wins"].append(player_blast)
        if len(game_state["player_last_wins"]) > 3:
            game_state["player_last_wins"].pop(0)  # Keep last 3 wins only

        game_state["player_last_level"] = player_blast
        if len(game_state["player_last_wins"]) >= 2:
            game_state["player_velocity"] = (
                game_state["player_last_wins"][-1] - game_state["player_last_wins"][-2]
            )
        else:
            game_state["player_velocity"] = 0

        if len(game_state["player_last_wins"]) >= 3:
            game_state["player_acceleration"] = (
                game_state["player_last_wins"][-1]
                - game_state["player_last_wins"][-2]
            ) - (
                game_state["player_last_wins"][-2]
                - game_state["player_last_wins"][-3]
            )
        else:
            game_state["player_acceleration"] = 0

        game_state["win_streak"] += 1
        game_state["loss_streak"] = 0
        game_state["waiting_for_blast"] = True  # Wait for player to select a blast
        return jsonify({'waiting_for_blast': True})  # Notify front-end

    else:
        # Update player stats on a loss
        game_state["win_streak"] = 0
        game_state["loss_streak"] += 1

        # Prepare input for bot
        input_data = pd.DataFrame([{
            "velocity": game_state["player_velocity"],
            "acceleration": game_state["player_acceleration"],
            "win_streak": game_state["win_streak"],
            "loss_streak": game_state["loss_streak"],
            "opponent_last_sound": game_state["player_last_level"],
            "opponent_velocity": game_state["player_velocity"],
            "opponent_acceleration": game_state["player_acceleration"]
        }])

        # Predict Bob's blast level
        bob_blast = bot_model.predict(input_data)[0]
        return jsonify({'bob_blast': int(round(bob_blast))})


@app.route('/set_player_blast', methods=['POST'])
def set_player_blast():
    data = request.json
    player_blast = data.get('player_blast', 0)
    game_state["player_last_level"] = player_blast
    game_state["waiting_for_blast"] = False  # Blast has been selected
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
