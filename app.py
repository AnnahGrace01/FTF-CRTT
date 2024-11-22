from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load the real bot model
bot_model = joblib.load('bot_model.pkl')

# Reset game state
def reset_game_state():
    return {
        'game_round': 0,
        'player_last_sound': 0,
        'prev_player_last_sound': 0,
        'player_velocity': 0,
        'prev_player_velocity': 0,
        'player_acceleration': 0,
        'bob_last_sound': 0,
        'prev_bob_last_sound': 0,
        'bob_velocity': 0,
        'prev_bob_velocity': 0,
        'bob_acceleration': 0,
        'bob_win_streak': 0,
        'bob_loss_streak': 0,
    }

# Initialize game state
game_state = reset_game_state()

# Logging helper
def log_game_state(action):
    print(f"--- {action} ---")
    print(f"Round: {game_state['game_round']}")
    print(f"Player's Last Sound: {game_state['player_last_sound']}")
    print(f"Player Velocity: {game_state['player_velocity']}")
    print(f"Player Acceleration: {game_state['player_acceleration']}")
    print(f"Bob Last Sound: {game_state['bob_last_sound']}")
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

    # Increment the round count
    game_state['game_round'] += 1

    player_won = player_reaction_time < bob_reaction_time

    if player_won:
        # Update Bob's streaks
        game_state['bob_loss_streak'] += 1
        game_state['bob_win_streak'] = 0

        # Update player stats for the next round
        if game_state['game_round'] > 1:
            game_state['player_velocity'] = game_state['player_last_sound'] - game_state['prev_player_last_sound']
        else:
            game_state['player_velocity'] = 0

        if game_state['game_round'] > 2:
            game_state['player_acceleration'] = game_state['player_velocity'] - game_state['prev_player_velocity']
        else:
            game_state['player_acceleration'] = 0

        log_game_state("Player Won - Waiting for Blast")
        return jsonify({'waiting_for_blast': True})

    else:
        # Update game state to prepare for Bob's decision
        prepare_bob_for_decision()

        # Predict Bob's blast level
        input_data = pd.DataFrame([[
            game_state['bob_velocity'],
            game_state['bob_acceleration'],
            game_state['bob_win_streak'],
            game_state['bob_loss_streak'],
            game_state['player_last_sound'],
            game_state['player_velocity'],
            game_state['player_acceleration']
        ]], columns=[
            'velocity', 'acceleration', 'win_streak', 'loss_streak',
            'opponent_last_sound', 'opponent_velocity', 'opponent_acceleration'
        ])
        bob_blast = int(bot_model.predict(input_data)[0])

        # Update Bob’s last sound
        game_state['prev_bob_last_sound'] = game_state['bob_last_sound']
        game_state['bob_last_sound'] = bob_blast

        log_game_state("Bob's Turn")
        return jsonify({'waiting_for_blast': False, 'bob_blast': bob_blast})

def prepare_bob_for_decision():
    """Update all relevant stats before Bob makes a decision."""
    global game_state
    if game_state['game_round'] > 1:
        game_state['bob_velocity'] = game_state['bob_last_sound'] - game_state['prev_bob_last_sound']
    else:
        game_state['bob_velocity'] = 0

    if game_state['game_round'] > 2:
        game_state['bob_acceleration'] = game_state['bob_velocity'] - game_state['prev_bob_velocity']
    else:
        game_state['bob_acceleration'] = 0

    game_state['prev_bob_velocity'] = game_state['bob_velocity']

@app.route('/set_player_blast', methods=['POST'])
def set_player_blast():
    global game_state

    data = request.json
    player_blast = data.get('player_blast', 0)

    # Update player's stats after their blast is given
    game_state['prev_player_velocity'] = game_state['player_velocity']
    game_state['prev_player_last_sound'] = game_state['player_last_sound']
    game_state['player_last_sound'] = player_blast

    log_game_state("Player Selected Blast")
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
