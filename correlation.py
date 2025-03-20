import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load merged dataset
merged_data = pd.read_pickle("cleaned_datasets_merged.pkl")

# Check if it's a dictionary and list available datasets
if isinstance(merged_data, dict):
    print("Available datasets in merged_data:", merged_data.keys())

    # Select the relevant dataset (adjust key if needed)
    merged_data = merged_data.get("Team Stats Per Game")

# Ensure it's a DataFrame
if not isinstance(merged_data, pd.DataFrame):
    raise TypeError("Selected dataset is not a DataFrame.")

# Drop non-numeric columns
numeric_data = merged_data.select_dtypes(include=["number"])

# Ensure 'pts_per_game' exists
if "pts_per_game" not in numeric_data.columns:
    raise KeyError("Column 'pts_per_game' not found in dataset.")

# Compute correlation of all numeric columns with 'pts_per_game'
correlation_with_pts = numeric_data.corr()["pts_per_game"].sort_values(ascending=False)

# Display top correlated features
print("Top correlations with Points Per Game:")
print(correlation_with_pts)

# Plot bar chart of correlations
plt.figure(figsize=(10, 6))
sns.barplot(x=correlation_with_pts.index, y=correlation_with_pts.values, palette="coolwarm")
plt.xticks(rotation=90)
plt.xlabel("Statistic")
plt.ylabel("Correlation with PTS per Game")
plt.title("Correlation of All Stats with Points Per Game")
plt.show()

# Define target variable
target = "pts_per_game"

# Define selected features
selected_features = [
    "fg_per_game", "fga_per_game", "x2p_percent", "ast_per_game",
    "fg_percent", "trb_per_game", "drb_per_game", "x2p_per_game",
    "ft_percent", "ft_per_game"
]

# Drop non-useful columns and keep only numerical data
df_clean = numeric_data[selected_features + [target]]

# Split into features (X) and target (y)
X = df_clean[selected_features]
y = df_clean[target]
