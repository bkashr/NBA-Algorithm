import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Step 1: Data Collection
# Load historical game data and player statistics
games_data = pd.read_csv('historical_games.csv')
players_data = pd.read_csv('player_stats.csv')

# Step 2: Data Preprocessing
# Merge game data with player statistics
data = pd.merge(games_data, players_data, on='game_id')

# Handle missing values
data.fillna(0, inplace=True)

# Step 3: Feature Engineering
# Create features for the model
data['total_points'] = data['home_team_points'] + data['away_team_points']
features = data[['home_team_points', 'away_team_points', 'home_team_rebounds', 'away_team_rebounds', 'home_team_assists', 'away_team_assists']]
target = data['total_points']

# Step 4: Model Training
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 5: Evaluation
# Predict on the test set
y_pred = model.predict(X_test)

# Calculate the mean squared error
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Step 6: Prediction
# Predict over/under totals for upcoming games
upcoming_games = pd.read_csv('upcoming_games.csv')
upcoming_features = upcoming_games[['home_team_points', 'away_team_points', 'home_team_rebounds', 'away_team_rebounds', 'home_team_assists', 'away_team_assists']]
predictions = model.predict(upcoming_features)

# Add predictions to the upcoming games data
upcoming_games['predicted_total_points'] = predictions

# Display the predictions
print(upcoming_games[['game_id', 'predicted_total_points']])