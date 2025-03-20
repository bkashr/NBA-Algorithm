import pandas as pd

# Load existing cleaned datasets (which is a dictionary)
cleaned_datasets = pd.read_pickle("cleaned_datasets.pkl")

# Load engineered team features (which is a DataFrame)
team_features = pd.read_pickle("team_features.pkl")

# Add team features to the dictionary
cleaned_datasets["Team Features"] = team_features

# Save the updated dictionary back to a pickle file
pd.to_pickle(cleaned_datasets, "cleaned_datasets_merged.pkl")

print("✅ Merging completed! Data saved as 'cleaned_datasets_merged.pkl'.")
