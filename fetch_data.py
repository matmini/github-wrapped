import os 
import requests 
import psycopg 
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

  # Create a table to store our wrapped data 
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS repositories (
        id SERIAL PRIMARY KEY, 
        name VARCHAR(255) UNIQUE NOT NULL,
        language VARCHAR(100),
        stars INTEGER DEFAULT 0
      );
  """)
  conn.commit()
  cursor.close()
  conn.close()
  print("📋 Database table verified/created successfully.")

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