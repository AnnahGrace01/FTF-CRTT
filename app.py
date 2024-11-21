from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Load the trained bot model
bot_model = joblib.load("bot_model.pkl")

# Create a Flask app
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    # Parse the JSON request data
    data = request.json

    # Extract features from the request
    velocity = data.get("velocity", 0)
    acceleration = data.get("acceleration", 0)
    win_streak = data.get("win_streak", 0)
    loss_streak = data.get("loss_streak", 0)
    opponent_last_sound = data.get("opponent_last_sound", 0)
    opponent_velocity = data.get("opponent_velocity", 0)
    opponent_acceleration = data.get("opponent_acceleration", 0)

    # Create a DataFrame for prediction
    input_data = pd.DataFrame({
        "velocity": [velocity],
        "acceleration": [acceleration],
        "win_streak": [win_streak],
        "loss_streak": [loss_streak],
        "opponent_last_sound": [opponent_last_sound],
        "opponent_velocity": [opponent_velocity],
        "opponent_acceleration": [opponent_acceleration]
    })

    # Get the predicted blast level
    predicted_blast = bot_model.predict(input_data)[0]

    # Return the prediction as JSON
    return jsonify({"blast_level": int(predicted_blast)})


if __name__ == '__main__':
    app.run(debug=True)
