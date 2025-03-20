import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Load cleaned dataset
df = pd.read_csv("cleaned_nba_games.csv")



# Define features (team stats)
features = [col for col in df.columns if col.startswith("team_a_") or col.startswith("team_b_")]

# Define target (points scored by Team A)
target = "team_a_pts"

# Split data into train/test sets
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

print(X_train.head())
print(X_train.dtypes)

X_train = pd.get_dummies(X_train, columns=["team_a_team_abbreviation", "team_b_team_abbreviation"])
X_test = pd.get_dummies(X_test, columns=["team_a_team_abbreviation", "team_b_team_abbreviation"])


X_train = X_train.drop(
    ["team_a_team_abbreviation", "team_a_team_name", "team_a_game_date",
     "team_b_team_abbreviation", "team_b_team_name", "team_b_game_date"],
    axis=1
)

X_test = X_test.drop(
    ["team_a_team_abbreviation", "team_a_team_name", "team_a_game_date",
     "team_b_team_abbreviation", "team_b_team_name", "team_b_game_date"],
    axis=1
)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

print(f"Model trained! MAE: {mae:.2f}")

# Save model
joblib.dump(model, "nba_score_predictor.pkl")

print("Model saved as 'nba_score_predictor.pkl'")
