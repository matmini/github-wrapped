import os 
import requests 
import psycopg 
import json 
from dotenv import load_dotenv 

# 1. Load the hidden secrets from the .env file 
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

# 2. Setup headers to tell GitHub who we are and format our request 
headers = {
  "Authorization": f"token {TOKEN}",
  "Accept": "application/vnd.github.v3+json"
}

def get_db_connection(): 
  """Establishes a connection to the PostgreSQL Docker container."""
  return psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
  )

def setup_database(): 
  """Creates a table for our repositories if it doesn't exist yet."""
  conn = get_db_connection()
  cursor = conn.cursor()

  # Verify/Create the repositories table 
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS repositories (
        id SERIAL PRIMARY KEY, 
        name VARCHAR(255) UNIQUE NOT NULL,
        language VARCHAR(100),
        stars INTEGER DEFAULT 0
      );
  """)

  # Verify/Create the commits table (Linked to repositories via fk) 
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS commits (
        id SERIAL PRIMARY KEY,
        sha VARCHAR(100) UNIQUE NOT NULL,
        repo_name VARCHAR(255) REFERENCES repositories(name) ON DELETE CASCADE,
        message TEXT,
        author_date TIMESTAMP
      );
  """)
  conn.commit()
  cursor.close()
  conn.close()
  print("Database tables verified/created successfully.")

def fetch_and_save_repos(): 
  """Fetches repos from GitHub and saves them to PostgreSQL."""
  url = "https://api.github.com/user/repos?per_page=100&type=owner"
  print("Fetching repositories from GitHub...")
  response = requests.get(url, headers=headers)

  if response.status_code != 200:
    print(f"GitHub error: {response.status_code}")
    print(f"Error details: {response.text}")
    return 
  
  repos = response.json()

  # Connect to the local Docker Postgres database 
  conn = get_db_connection()
  cursor = conn.cursor() 

  print(f"Saving {len(repos)} repositories to Docker database...") 

  for repo in repos: 
    name = repo.get("name")
    lang = repo.get("language") or "Unknown"
    stars = repo.get("stargazers_count") or 0 
  
    # Insert data, or update if the repository name already exists (upsert)
    cursor.execute("""
      INSERT INTO repositories (name, language, stars)
      VALUES (%s, %s, %s)
      ON CONFLICT (name)
      DO UPDATE SET language = EXCLUDED.language, stars = EXCLUDED.stars;
    """, (name, lang, stars))
  
  conn.commit()
  cursor.close()
  conn.close()
  print("All data successfully synced to the database!")
  
def fetch_and_save_commits(): 
  """Fetches commit history for our saved repositories and stores them."""
  conn = get_db_connection()
  cursor = conn.cursor()

  # 1. Grab all the repository names currently in our database 
  cursor.execute("SELECT name FROM repositories;")
  repos = cursor.fetchall()

  # We will need your GitHub username to build the repo path 
  # Let's fetch your username dynamically from the API to make it robust 
  profile_response = requests.get("https://api.github.com/user", headers=headers)
  username = profile_response.json().get("login") 

  print(f"[FETCH] Beginning commit sync for {len(repos)} repositories...")

  for row in repos: 
    repo_name = row[0] # name
    # GitHub endpoint format: /repos/{owner}/{repo}/commits 
    url = f"https://api.github.com/repos/{username}/{repo_name}/commits?per_page=50" 
    
    print(f"[FETCH] Querying commits for: {repo_name}...")
    response = requests.get(url, headers=headers) 

    if response.status_code != 200:
      print(f"[ERROR] Could not fetch commits for {repo_name}. Status {response.status}")
      continue 

    commits = response.json() 
    print(f"[DATA] Found {len(commits)} commits for {repo_name}") 



def test_github_connection(): 
  # 3. Request your authenticated user infro from the GitHub API 
  url = "https://api.github.com/user"
  print("Connecting to GitHub API...")
  response = requests.get(url, headers=headers) 

  # 4. Check if the server responded with HTTP 200 (OK/Success) 
  if response.status_code == 200: 
    data = response.json()
    print("\nConnection Successful!")
    print(f"Logged in as: {data.get('login')}")
    print(f"Name: {data.get('name')}")
    print(f"Public Repos: {data.get('public_repos')}")
    print(f"Organizations: {data.get('organizations_url')}")
    print(f"Bio: {data.get('bio')}")
  else: 
    print(f"\nFailed to connect. Status Code: {response.status_code}")
    print(f"Error Message: {response.text}")

if __name__ == "__main__":
  print("Testing database connection and table creation...")
  setup_database()
  fetch_and_save_repos()
  fetch_and_save_commits()