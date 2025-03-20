import pandas as pd
import numpy as np
import joblib  # To save the model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Load your cleaned dataset (Make sure this points to the correct file)
df = pd.read_csv("cleaned_nba_data.csv")  # Use the dataset after processing

# Define target variable
target = "pts_per_game"

# Define selected features
selected_features = [
    "fg_per_game", "fga_per_game", "x2p_percent", "ast_per_game",
    "fg_percent", "trb_per_game", "drb_per_game", "x2p_per_game",
    "ft_percent", "ft_per_game"
]

# Split data into features (X) and target (y)
X = df[selected_features]
y = df[target]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize & Train Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate Model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae:.2f}")
print(f"R-squared Score: {r2:.2f}")

# Save the trained model
joblib.dump(model, "nba_score_predictor.pkl")

print("Model saved as nba_score_predictor.pkl")
