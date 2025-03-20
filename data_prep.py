import pandas as pd

# Load the dataset
df = pd.read_csv("nba_games_2023_24.csv")

# Split MATCHUP into team names
df[["Team A", "Team B"]] = df["MATCHUP"].str.split(r" vs\.? ", expand=True)

# Drop unnecessary columns
df = df.drop(["MATCHUP", "WL", "VIDEO_AVAILABLE", "MIN", "PLUS_MINUS"], axis=1, errors="ignore")

# Rename columns for clarity (Team A stats)
stat_columns = df.columns.difference(["Team A", "Team B"])
df = df.rename(columns={col: f"team_a_{col.lower()}" for col in stat_columns})

# Create a copy for Team B stats and rename appropriately
df_b = df.copy()
df_b = df_b.rename(columns={col: col.replace("team_a_", "team_b_") for col in df.columns if "team_a_" in col})

# Swap Team A and Team B for df_b
df_b[["Team A", "Team B"]] = df[["Team B", "Team A"]]

# Combine both perspectives
df_combined = pd.concat([df, df_b], ignore_index=True)

# Save cleaned dataset
df_combined.to_csv("cleaned_nba_games.csv", index=False)

print("Data preparation complete! Saved as 'cleaned_nba_games.csv'")
