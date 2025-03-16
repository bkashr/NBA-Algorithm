import pandas as pd
import pickle
import os

# Define file paths (update these paths to match where your CSVs are stored)
file_paths = {
    "Team Stats Per Game": "Team Stats Per Game.csv",
    "Team Totals": "Team Totals.csv",
    "Opponent Stats Per Game": "Opponent Stats Per Game.csv",
    "Opponent Totals": "Opponent Totals.csv",
    "Player Per Game": "Player Per Game.csv",
    "Player Play By Play": "Player Play By Play.csv",
    "Player Shooting": "Player Shooting.csv",
    "Team Stats Per 100 Poss": "Team Stats Per 100 Poss.csv"
}

# Load datasets
datasets = {}
for name, path in file_paths.items():
    if os.path.exists(path):  # Check if file exists
        datasets[name] = pd.read_csv(path)
    else:
        print(f"Warning: {path} not found, skipping.")

# Define season range (last 10 years)
latest_season = 2024  # Adjust this to the current season
min_season = latest_season - 9

# Clean datasets
for name, df in datasets.items():
    # Drop rows with missing values
    df.dropna(inplace=True)

    # Filter for the last 10 seasons if a 'Season' column exists
    if 'Season' in df.columns:
        df = df[df['Season'].between(min_season, latest_season)]

    # Remove players who played 0 minutes (only for player datasets)
    if 'MP' in df.columns and 'Player' in df.columns:
        df = df[df['MP'] > 0]

    # Save cleaned data back to dictionary
    datasets[name] = df

# Save cleaned datasets using pickle
with open("cleaned_datasets.pkl", "wb") as f:
    pickle.dump(datasets, f)

print("Data collection and cleaning completed successfully!")
