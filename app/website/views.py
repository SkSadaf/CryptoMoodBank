from flask import Blueprint, render_template, request, jsonify
import pandas as pd
from app.website.models.model_2 import model  # Import your trained model

views = Blueprint('views', __name__)

@views.route('/')
# this function will run whenever 
# we are in our home url
def home():
    return render_template("home.html")

@views.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        interaction_count = int(data['interaction_count'])
        streak_count = int(data['streak_count'])
        volatility_score = float(data['volatility_score'])
        
        # Prepare input for prediction
        user_input = pd.DataFrame({
            'interaction_count': [interaction_count],
            'streak_count': [streak_count],
            'volatility_score': [volatility_score]
        })
        
        # Predict
        predicted_coins = model.predict(user_input)
        return jsonify({'predicted_coins': predicted_coins[0]})
    except Exception as e:
        return jsonify({'error': str(e)})
