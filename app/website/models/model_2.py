import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Simulated dataset
data = pd.DataFrame({
    'interaction_count': [5, 10, 15, 20, 25, 30, 35, 40],
    'streak_count': [1, 3, 5, 7, 10, 12, 15, 18],
    'volatility_score': [0.8, 0.5, 0.3, 0.2, 0.1, 0.05, 0.03, 0.02],
    'coin_reward': [5, 8, 10, 12, 15, 18, 20, 25]  # Target: predicted coins
})

# Features and target
X = data[['interaction_count', 'streak_count', 'volatility_score']]
y = data['coin_reward']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluate Model
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse:.2f}")

# Function to take dynamic input and predict coin rewards
# Function to take dynamic input and predict coin rewards
def predict_dynamic():
    print("\nEnter the following details to predict your coin reward:")
    try:
        interaction_count = int(input("Interaction Count (e.g., 12): "))
        streak_count = int(input("Streak Count (e.g., 4): "))
        volatility_score = float(input("Volatility Score (e.g., 0.4): "))
        
        # Prepare the input for prediction
        user_input = pd.DataFrame({
            'interaction_count': [interaction_count],
            'streak_count': [streak_count],
            'volatility_score': [volatility_score]
        })
        
        # Predict the coin reward
        predicted_coins = model.predict(user_input)
        print(f"Predicted Coins for the given inputs: {predicted_coins[0]:.2f}")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

# Call the function to allow user interaction
predict_dynamic()
