from flask import Flask, request, jsonify
import random
import pandas as pd

app = Flask(__name__)

# Dummy model for Bob's decision (replace with actual model)
def bot_decision(input_data):
    return random.randint(1, 8)

# Game state
game_state = {
    'velocity': 0,
    'acceleration': 0,
    'win_streak': 0,
    'loss_streak': 0,
    'opponent_last_sound': 0,
    'opponent_velocity': 0,
    'opponent_acceleration': 0
}

# Logging helper
def log_game_state(action):
    print(f"--- {action} ---")
    print(f"Player's Last Blast: {game_state['opponent_last_sound']}")
    print(f"Velocity: {game_state['velocity']}")
    print(f"Acceleration: {game_state['acceleration']}")
    print(f"Win Streak: {game_state['win_streak']}")
    print(f"Loss Streak: {game_state['loss_streak']}")
    print("-------------------")

@app.route('/play_round', methods=['POST'])
def play_round():
    global game_state

    data = request.json
    player_reaction_time = data.get('reaction_time', float('inf'))  # Default to inf if not provided
    bob_reaction_time = 500  # Bob's constant reaction time in milliseconds

    player_won = player_reaction_time < bob_reaction_time

    # Update game state
    if player_won:
        game_state['win_streak'] += 1
        game_state['loss_streak'] = 0
    else:
        game_state['win_streak'] = 0
        game_state['loss_streak'] += 1

    if not player_won:
        # Bob decides blast level
        input_data = pd.DataFrame([[
            game_state['velocity'],
            game_state['acceleration'],
            game_state['win_streak'],
            game_state['loss_streak'],
            game_state['opponent_last_sound'],
            game_state['opponent_velocity'],
            game_state['opponent_acceleration']
        ]], columns=[
            'velocity', 'acceleration', 'win_streak', 'loss_streak',
            'opponent_last_sound', 'opponent_velocity', 'opponent_acceleration'
        ])
        bob_blast = bot_decision(input_data)
        game_state['opponent_last_sound'] = bob_blast

        log_game_state("Bob's Turn")
        return jsonify({'waiting_for_blast': False, 'bob_blast': bob_blast})

    log_game_state("Player Won - Waiting for Blast")
    return jsonify({'waiting_for_blast': True})

@app.route('/set_player_blast', methods=['POST'])
def set_player_blast():
    global game_state

    data = request.json
    player_blast = data.get('player_blast', 0)

    # Update player stats
    if game_state['win_streak'] >= 2:
        game_state['velocity'] = player_blast - game_state['opponent_last_sound']
    else:
        game_state['velocity'] = 0

    if game_state['win_streak'] >= 3:
        game_state['acceleration'] = game_state['velocity'] - game_state['opponent_velocity']
    else:
        game_state['acceleration'] = 0

    game_state['opponent_last_sound'] = player_blast
    game_state['opponent_velocity'] = game_state['velocity']
    game_state['opponent_acceleration'] = game_state['acceleration']

    log_game_state("Player Selected Blast")
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
