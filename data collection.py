import requests
import pandas as pd
from datetime import datetime

# Function to fetch player injury data from an API
def fetch_injury_data(api_url, api_key):
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

# Function to update the player statistics with injury data
def update_player_stats(player_stats, injury_data):
    for injury in injury_data:
        player_id = injury['player_id']
        status = injury['status']
        player_stats.loc[player_stats['player_id'] == player_id, 'injury_status'] = status
    return player_stats

# Example usage
api_url = 'https://api.sportsdata.io/v3/nba/scores/json/Injuries'
api_key = 'your_api_key_here'
injury_data = fetch_injury_data(api_url, api_key)

# Load existing player statistics
player_stats = pd.read_csv('player_stats.csv')

# Update player statistics with injury data
updated_player_stats = update_player_stats(player_stats, injury_data)

# Save the updated player statistics
updated_player_stats.to_csv('updated_player_stats.csv', index=False)