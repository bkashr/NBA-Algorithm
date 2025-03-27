import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time
import random
from datetime import datetime, timedelta
import json

# Create directories if they don't exist
os.makedirs("team_stats", exist_ok=True)
os.makedirs("cache", exist_ok=True)

# Headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.requests_per_minute = 0
        self.last_request_time = datetime.now()
        self.request_times = []
        self.load_progress()
        
    def load_progress(self):
        """Load progress from file if it exists"""
        if os.path.exists('scraping_progress.json'):
            with open('scraping_progress.json', 'r') as f:
                self.progress = json.load(f)
        else:
            self.progress = {
                'last_year': None,
                'banned_until': None
            }
            
    def save_progress(self):
        """Save current progress to file"""
        with open('scraping_progress.json', 'w') as f:
            json.dump(self.progress, f)
            
    def create_new_session(self):
        """Create a new session after 15 requests (more conservative)"""
        self.session = requests.Session()
        self.session.headers.update(headers)
        print("Created new session")
        
    def get_cached_content(self, url):
        """Check if content is cached and return it if available"""
        cache_file = f"cache/{url.split('/')[-1]}"
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None
        
    def cache_content(self, url, content):
        """Cache the content for future use"""
        cache_file = f"cache/{url.split('/')[-1]}"
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def maintain_rate_limit(self):
        """Maintain approximately 15 requests per minute (more conservative)"""
        current_time = datetime.now()
        
        # Remove requests older than 1 minute
        self.request_times = [t for t in self.request_times if current_time - t < timedelta(minutes=1)]
        
        # If we've made 15 requests in the last minute, wait
        while len(self.request_times) >= 15:
            time.sleep(1)
            current_time = datetime.now()
            self.request_times = [t for t in self.request_times if current_time - t < timedelta(minutes=1)]
            
        # Add current request time
        self.request_times.append(current_time)
        
    def download_with_retry(self, url, max_retries=3):
        """Download content with rate limiting and retries"""
        # Check cache first
        cached_content = self.get_cached_content(url)
        if cached_content:
            print(f"Using cached content for {url}")
            return cached_content
            
        for attempt in range(max_retries):
            try:
                # Check if we're banned
                if self.progress['banned_until']:
                    banned_until = datetime.fromisoformat(self.progress['banned_until'])
                    if datetime.now() < banned_until:
                        wait_time = (banned_until - datetime.now()).total_seconds()
                        print(f"Currently banned. Waiting {wait_time/3600:.1f} hours...")
                        time.sleep(wait_time)
                    else:
                        self.progress['banned_until'] = None
                        self.save_progress()
                
                # Maintain rate limit
                self.maintain_rate_limit()
                
                # Create new session every 15 requests (more conservative)
                if self.requests_per_minute >= 15:
                    self.create_new_session()
                    self.requests_per_minute = 0
                
                response = self.session.get(url)
                response.raise_for_status()
                
                # Cache the successful response
                self.cache_content(url, response.text)
                return response.text
                
            except requests.exceptions.RequestException as e:
                if "429" in str(e):
                    # If we get rate limited, assume we're banned for 24 hours
                    banned_until = datetime.now() + timedelta(hours=24)
                    self.progress['banned_until'] = banned_until.isoformat()
                    self.save_progress()
                    print("Rate limit hit. Banned for 24 hours. Progress saved.")
                    raise e
                    
                if attempt == max_retries - 1:
                    raise e
                delay = 60 * (2 ** attempt)  # Longer exponential backoff
                print(f"Attempt {attempt + 1} failed. Waiting {delay} seconds before retrying...")
                time.sleep(delay)

# Initialize scraper
scraper = Scraper()

years = list(range(2000,2025))
url_start = "https://www.basketball-reference.com/leagues/NBA_{}.html#all_per_game_team-opponent"

# Download HTML files with rate limiting
for year in years:
    # Skip years we've already processed
    if scraper.progress['last_year'] and year <= scraper.progress['last_year']:
        print(f"Skipping {year} (already processed)")
        continue
        
    url = url_start.format(year)
    try:
        print(f"Downloading data for {year}...")
        html_content = scraper.download_with_retry(url)
        
        with open(f"team_stats/{year}.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        # Update progress
        scraper.progress['last_year'] = year
        scraper.save_progress()
            
    except Exception as e:
        print(f"Error downloading data for {year}: {str(e)}")
        if "429" in str(e):
            print("Rate limit hit. Script will resume from last successful year when run again.")
            break
        continue

# Process the downloaded files
dfs = []
for year in years:
    try:
        with open(f"team_stats/{year}.html", "r", encoding="utf-8") as f:
            page = f.read()
        
        soup = BeautifulSoup(page, "html.parser")
        totals = soup.find(id="totals-team")
        
        if totals is None:
            print(f"Warning: Could not find totals table for {year}")
            continue
            
        totals_df = pd.read_html(StringIO(str(totals)))[0]
        totals_df['Year'] = year
        dfs.append(totals_df)
        
    except Exception as e:
        print(f"Error processing data for {year}: {str(e)}")
        continue

if dfs:
    # Combine all dataframes
    final_df = pd.concat(dfs, ignore_index=True)
    final_df.to_csv("totals.csv", index=False)
    print("Successfully saved data to totals.csv")
else:
    print("No data was successfully processed")

