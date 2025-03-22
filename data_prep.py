import pandas as pd

# Load the dataset
df = pd.read_csv("nba_games_2023_24.csv")

# Split MATCHUP into team names
df[["Team A", "Team B"]] = df["MATCHUP"].str.split(r" vs\.? ", expand=True)

# Drop unnecessary columns
df = df.drop(["MATCHUP", "WL", "VIDEO_AVAILABLE", "MIN", "PLUS_MINUS"], axis=1, errors="ignore")

# Store original column names
original_columns = df.columns.tolist()

# Rename columns for Team A stats
stat_columns = df.columns.difference(["Team A", "Team B"])
df = df.rename(columns={col: f"team_a_{col.lower()}" for col in stat_columns})

# Create a copy for Team B stats before renaming
df_b = df.copy()

# Swap Team A and Team B names
df_b[["Team A", "Team B"]] = df[["Team B", "Team A"]]

# Merge back the actual stats for Team B from the original dataset
df_b = df_b.merge(
    df.rename(columns=lambda x: x.replace("team_a_", "team_b_")),
    left_on="Team B",
    right_on="Team A",
    how="left",
    suffixes=("", "_b")
)

# Drop redundant columns from the merge
df_b = df_b.drop(columns=[col for col in df_b.columns if col.endswith("_b")])

# Debugging: Print sample rows before merging
print("Sample of df (Team A stats):")
print(df.head(3))
print("\nSample of df_b (Team B stats - properly mapped):")
print(df_b.head(3))

# Ensure Team B now has valid statistics before merging
print("\nChecking for missing values in df_b:")
print(df_b.isnull().sum())

# Combine both perspectives
df_combined = pd.concat([df, df_b], ignore_index=True)

# Debugging: Print sample of final dataset
print("\nFinal dataset sample after merging:")
print(df_combined.head(5))

# Save cleaned dataset
df_combined.to_csv("cleaned_nba_games_fixed.csv", index=False)

print("✅ Data preparation complete! Saved as 'cleaned_nba_games.csv'")
