import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_pickle("cleaned_datasets.pkl")

# Print available datasets
print("Available datasets:", data.keys())

# Extract relevant datasets
team_stats = data["Team Stats Per Game"]
team_totals = data["Team Totals"]

# Check available columns
print("Columns in Team Stats Per Game:", team_stats.columns)
print("Columns in Team Totals:", team_totals.columns)

# Use total games played (`g`) as a proxy for wins (for now)
team_stats["wins_estimate"] = team_stats["g"] * 0.5  # Placeholder (adjust if needed)

# Set seaborn style
sns.set_style("whitegrid")

# **1. Plot Offensive Efficiency vs Estimated Wins**
plt.figure(figsize=(10, 6))
sns.scatterplot(x=team_stats["pts_per_game"] / (team_stats["tov_per_game"] + 1), 
                y=team_stats["wins_estimate"], 
                hue=team_stats["team"], 
                palette="viridis", s=100)
plt.xlabel("Offensive Efficiency (PTS / (TOV + 1))")
plt.ylabel("Estimated Wins")
plt.title("Offensive Efficiency vs. Estimated Wins")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.show()

# **2. Plot Team Points Per Game vs Key Stats**
plt.figure(figsize=(12, 6))
sns.pairplot(team_stats, vars=["pts_per_game", "fg_per_game", "x3p_per_game", "fta_per_game"], 
             diag_kind="kde", corner=True)
plt.suptitle("Scoring Indicators: PPG vs. Shooting Stats", y=1.02)
plt.show()

# **3. Correlation Heatmap of Scoring Indicators**
plt.figure(figsize=(10, 6))
scoring_stats = team_stats[["pts_per_game", "fg_per_game", "x3p_per_game", "fta_per_game", "tov_per_game"]]
sns.heatmap(scoring_stats.corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Heatmap of Scoring Indicators")
plt.show()
