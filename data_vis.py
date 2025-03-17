import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
team_stats = pd.read_csv("cleaned_team_stats.csv")  # Adjust file name if different

# 1. Histogram of key stats
team_stats.hist(figsize=(12, 8), bins=20)
plt.suptitle("Feature Distributions", fontsize=14)
plt.show()

# 2. Correlation heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(team_stats.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlations")
plt.show()

# 3. Scatter plot: Field Goal Attempts vs. Points per Game
plt.figure(figsize=(8, 5))
sns.scatterplot(x=team_stats["fga_per_game"], y=team_stats["pts_per_game"])
plt.xlabel("Field Goal Attempts per Game")
plt.ylabel("Points per Game")
plt.title("FGA vs. PTS")
plt.show()

# 4. Line graph of offensive efficiency over seasons
plt.figure(figsize=(10, 5))
sns.lineplot(x=team_stats["season"], y=team_stats["offensive_efficiency"], marker="o")
plt.xlabel("Season")
plt.ylabel("Offensive Efficiency")
plt.title("Offensive Efficiency Over Time")
plt.xticks(rotation=45)
plt.show()
