from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load the pre-trained bot model
bot_model = joblib.load('bot_model.pkl')

# Initialize game state
game_state = {
    'game_round': 0,
    'player_last_sound': None,
    'player_velocity': None,
    'player_acceleration': None,
    'bob_last_sound': None,
    'bob_velocity': None,
    'bob_acceleration': None,
    'bob_win_streak': 0,
    'bob_loss_streak': 0,
    'prev_player_last_sound': None,
    'prev_player_velocity': None,
    'prev_bob_last_sound': None,
    'prev_bob_velocity': None,
    'bob_wins': 0,
    'player_wins': 0,
}


def log_game_state(message):
    """Logs the current state of the game."""
    print(message)
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


def log_bob_inputs():
    """Logs the inputs Bob receives for making a decision."""
    print("Bob's Decision Inputs:")
    print(f"Player Last Sound: {game_state['player_last_sound']}")
    print(f"Player Velocity: {game_state['player_velocity']}")
    print(f"Player Acceleration: {game_state['player_acceleration']}")
    print(f"Bob Last Sound: {game_state['bob_last_sound']}")
    print(f"Bob Velocity: {game_state['bob_velocity']}")
    print(f"Bob Acceleration: {game_state['bob_acceleration']}")
    print(f"Bob Win Streak: {game_state['bob_win_streak']}")
    print(f"Bob Loss Streak: {game_state['bob_loss_streak']}")
    print("-------------------")


def prepare_bob_for_decision():
    """Prepare all relevant stats before Bob makes a decision."""
    global game_state

    # Ensure Bob's velocity and acceleration are updated correctly after a win
    if game_state['bob_win_streak'] >= 2:
        # Bob's velocity: change in sound from the previous to the current round
        game_state['bob_velocity'] = game_state['bob_last_sound'] - game_state['prev_bob_last_sound']
    else:
        game_state['bob_velocity'] = None

    if game_state['bob_win_streak'] >= 3:
        # Bob's acceleration: change in velocity from the previous to the current round
        game_state['bob_acceleration'] = game_state['bob_velocity'] - game_state['prev_bob_velocity']
    else:
        game_state['bob_acceleration'] = None

    # Update the "previous" values for the next round
    game_state['prev_bob_last_sound'] = game_state['bob_last_sound']
    game_state['prev_bob_velocity'] = game_state['bob_velocity']

    # Log Bob's decision inputs
    print(f"Bob's Decision Inputs:")
    print(f"Player Last Sound: {game_state['player_last_sound']}")
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
        # Update Player's stats
        game_state['player_wins'] += 1
        game_state['bob_loss_streak'] += 1
        game_state['bob_win_streak'] = 0

        log_game_state("Player Won - Waiting for Blast")
        return jsonify({'waiting_for_blast': True})

    else:
        # Update Bob's stats
        game_state['bob_wins'] += 1
        game_state['bob_win_streak'] += 1
        game_state['bob_loss_streak'] = 0

        # Prepare Bob's inputs
        prepare_bob_for_decision()

        # Predict Bob's blast level
        input_data = pd.DataFrame([[
            game_state['bob_velocity'] or 0,
            game_state['bob_acceleration'] or 0,
            game_state['bob_win_streak'],
            game_state['bob_loss_streak'],
            game_state['player_last_sound'] or 0,
            game_state['player_velocity'] or 0,
            game_state['player_acceleration'] or 0
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


@app.route('/set_player_blast', methods=['POST'])
def set_player_blast():
    global game_state

    data = request.json
    player_blast = int(data.get('player_blast', game_state['player_last_sound'] or 0))
    game_state['prev_player_last_sound'] = game_state['player_last_sound']
    game_state['player_last_sound'] = player_blast

    if game_state['player_wins'] >= 2 and game_state['prev_player_last_sound'] is not None:
        game_state['player_velocity'] = game_state['player_last_sound'] - game_state['prev_player_last_sound']
    else:
        game_state['player_velocity'] = None

    if game_state['player_wins'] >= 3 and game_state['prev_player_velocity'] is not None:
        game_state['player_acceleration'] = game_state['player_velocity'] - game_state['prev_player_velocity']
    else:
        game_state['player_acceleration'] = None

    game_state['prev_player_velocity'] = game_state['player_velocity']

    log_game_state("Player Selected Blast")
    return ('', 204)


if __name__ == '__main__':
    app.run(debug=True)
