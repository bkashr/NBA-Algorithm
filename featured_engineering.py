import pandas as pd

# Load cleaned dataset
datasets = pd.read_pickle("cleaned_datasets.pkl")

# Extract team stats
team_stats = datasets['Team Stats Per Game']

# Debugging: Check available columns
print("Available columns in team_stats:", team_stats.columns)

# Ensure column names are clean (remove extra spaces)
team_stats.columns = team_stats.columns.str.strip()

# Rename columns for consistency
column_mapping = {
    "pts_per_game": "PTS",
    "fga_per_game": "FGA",
    "fta_per_game": "FTA",
    "orb_per_game": "ORB",
    "tov_per_game": "TOV",
    "g": "G"
}
team_stats.rename(columns=column_mapping, inplace=True)

# Verify required columns exist
required_columns = ["PTS", "FGA", "FTA", "ORB", "TOV", "G"]
missing_columns = [col for col in required_columns if col not in team_stats.columns]
if missing_columns:
    raise KeyError(f"Missing required columns: {missing_columns}")

# Feature Engineering: Calculate Offensive and Defensive Efficiency
team_stats["Offensive Efficiency"] = team_stats["PTS"] / team_stats["FGA"]
team_stats["Possessions"] = team_stats["FGA"] + 0.44 * team_stats["FTA"] - team_stats["ORB"] + team_stats["TOV"]
team_stats["Pace"] = team_stats["Possessions"] / team_stats["G"]

# Save engineered features
team_stats.to_pickle("team_features.pkl")

print("✅ Feature Engineering Completed! Data saved as 'team_features.pkl'.")
