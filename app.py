from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the actual bot model
bot_model = joblib.load("bot_model.pkl")

# Game state
game_state = {
    'player_last_sound': 0,
    'player_velocity': 0,
    'player_acceleration': 0,
    'bob_velocity': 0,
    'bob_acceleration': 0,
    'bob_win_streak': 0,
    'bob_loss_streak': 0,
    'bob_last_loss_streak': 0,
    'bob_last_win_streak': 0,
    'player_win_history': []  # Tracks player's winning blasts for velocity/acceleration calculations
}

# Logging helper
def log_game_state(action):
    print(f"--- {action} ---")
    print(f"Player's Last Sound: {game_state['player_last_sound']}")
    print(f"Player Velocity: {game_state['player_velocity']}")
    print(f"Player Acceleration: {game_state['player_acceleration']}")
    print(f"Bob Velocity: {game_state['bob_velocity']}")
    print(f"Bob Acceleration: {game_state['bob_acceleration']}")
    print(f"Bob Win Streak: {game_state['bob_win_streak']}")
    print(f"Bob Loss Streak: {game_state['bob_loss_streak']}")
    print("-------------------")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play_round', methods=['POST'])
def play_round():
    global game_state

    data = request.json
    player_reaction_time = data.get('reaction_time', float('inf'))  # Default to inf if not provided
    bob_reaction_time = 500  # Bob's constant reaction time in milliseconds

    player_won = player_reaction_time < bob_reaction_time

    if player_won:
        # Update player win history
        game_state['bob_loss_streak'] += 1
        game_state['bob_last_win_streak'] = game_state['bob_win_streak']
        game_state['bob_win_streak'] = 0

        # Update player stats
        if game_state['player_win_history']:
            last_two = game_state['player_win_history'][-2:]
            if len(last_two) == 2:
                game_state['player_velocity'] = last_two[1] - last_two[0]
            else:
                game_state['player_velocity'] = 0
            if len(game_state['player_win_history']) >= 3:
                game_state['player_acceleration'] = (
                    game_state['player_velocity']
                    - (last_two[0] - game_state['player_win_history'][-3])
                )
            else:
                game_state['player_acceleration'] = 0
        else:
            game_state['player_velocity'] = 0
            game_state['player_acceleration'] = 0

        log_game_state("Player Won - Waiting for Blast")
        return jsonify({'waiting_for_blast': True})
    else:
        # Bob's turn
        game_state['bob_win_streak'] += 1
        game_state['bob_last_loss_streak'] = game_state['bob_loss_streak']
        game_state['bob_loss_streak'] = 0

        # Update Bob's stats
        input_data = pd.DataFrame([[
            game_state['bob_velocity'],
            game_state['bob_acceleration'],
            game_state['bob_win_streak'],
            game_state['bob_last_loss_streak'],
            game_state['player_last_sound'],
            game_state['player_velocity'],
            game_state['player_acceleration']
        ]], columns=[
            'velocity', 'acceleration', 'win_streak', 'loss_streak',
            'opponent_last_sound', 'opponent_velocity', 'opponent_acceleration'
        ])
        bob_blast = int(bot_model.predict(input_data)[0])
        game_state['bob_velocity'] = bob_blast - game_state['player_last_sound']
        if game_state['bob_win_streak'] > 1:
            game_state['bob_acceleration'] = (
                game_state['bob_velocity'] - game_state['bob_velocity']
            )
        else:
            game_state['bob_acceleration'] = 0

        game_state['player_last_sound'] = bob_blast
        log_game_state("Bob's Turn")
        return jsonify({'waiting_for_blast': False, 'bob_blast': bob_blast})


@app.route('/set_player_blast', methods=['POST'])
def set_player_blast():
    global game_state

    data = request.json
    player_blast = data.get('player_blast', 0)

    # Add player's blast to win history
    game_state['player_win_history'].append(player_blast)
    if len(game_state['player_win_history']) > 3:
        game_state['player_win_history'] = game_state['player_win_history'][-3:]

    game_state['player_last_sound'] = player_blast

    log_game_state("Player Selected Blast")
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
