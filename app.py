import os
import pandas as pd
import joblib
from flask import Flask, request, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)

# Load the bot model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "bot_model.pkl")
bot_model = joblib.load(MODEL_PATH)

# Game state variables
velocity = 0
acceleration = 0
win_streak = 0
loss_streak = 0
opponent_last_sound = 0
opponent_velocity = 0
opponent_acceleration = 0

# Main page route
@app.route('/')
def home():
    return render_template('index.html')  # Loads the frontend HTML

# Play round route
@app.route('/play_round', methods=['POST'])
def play_round():
    global velocity, acceleration, win_streak, loss_streak, opponent_last_sound, opponent_velocity, opponent_acceleration

    # Receive data from the frontend
    data = request.json
    print("Received data from player:", data)  # Debug log

    player_blast = int(data.get('player_blast', 0))
    player_won = data.get('player_won', False)

    # Update win/loss streaks
    if player_won:
        win_streak += 1
        loss_streak = 0
    else:
        win_streak = 0
        loss_streak += 1

    # Update velocity and acceleration
    opponent_velocity = player_blast - opponent_last_sound
    opponent_acceleration = opponent_velocity - velocity
    velocity = opponent_velocity
    acceleration = opponent_acceleration
    opponent_last_sound = player_blast

    # If Bob needs to make a decision
    if not player_won:
        input_data = pd.DataFrame({
            'velocity': [velocity],
            'acceleration': [acceleration],
            'win_streak': [win_streak],
            'loss_streak': [loss_streak],
            'opponent_last_sound': [opponent_last_sound],
            'opponent_velocity': [opponent_velocity],
            'opponent_acceleration': [opponent_acceleration]
        })
        print("Input data for bot model:", input_data)  # Debug log

        # Predict Bob's blast level
        bob_blast = bot_model.predict(input_data)[0]
        print("Bob's blast level:", bob_blast)  # Debug log

        return jsonify({'bob_blast': int(round(bob_blast))})

    return jsonify({})

# Debugging endpoint to verify the server is running
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Running!'})

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
