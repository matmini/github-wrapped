import os 
import psycopg
from dotenv import load_dotenv 

# Load database credentials 
load_dotenv() 

def view_repositories():
  """Queries the PostgreSQL database and isplays saved data."""

  # Connect using psycopg 
  conn = psycopg.connect(
    host = os.getenv("DB_HOST"), 
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"), 
    password=os.getenv("DB_PASSWORD")
  )

  cursor = conn.cursor() 

  # Query to select all entries from out table 
  cursor.execute("SELECT username, id, name, language, stars FROM repositories ORDER BY stars DESC;")
  rows = cursor.fetchall() 

  print("\n --- DATABASE ENTRIES (Sorted by Stars) --- ")
  print(f"{'Username':<15} | {'ID':<5} | {'Repository Name':<30} | {'Language':<15} | {'Stars':<5} ")
  print("-"* 65) 

  for row in rows:
    print(f"{row[0]:<15} | {row[1]:<5} | {row[2]:<30} | {row[3]:<15} | {row[4]:<5}")
        
  print(f"---------------------------------------------\nTotal rows found: {len(rows)}\n")
    
  cursor.close()
  conn.close()

def view_commits():
  """Queries the PostgreSQL and displays the commits"""
  
  # Connect using psycopg 
  conn = psycopg.connect(
    host = os.getenv("DB_HOST"), 
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"), 
    password=os.getenv("DB_PASSWORD")
  )

  cursor = conn.cursor() 

    # Query to select all entries from out table 
  cursor.execute("SELECT sha, repo_name , message, author_date FROM commits ORDER BY author_date DESC LIMIT 20;")
  rows = cursor.fetchall() 

  print("\n --- DATABASE ENTRIES (Sorted by Date) --- ")
  print(f"{'sha':<40} | {'Repository Name':<20} | {'Message':<100} | {'Date':} ")
  print("-"* 65) 

  for row in rows:
    short_sha = row[0][:10] # first ten chars 
    repo = row[1]
    msg = row[2].replace("\n", " ") #truncate long commit messages
    short_msg = msg[:30] + "..." if len(msg) > 30 else msg
    raw_date = row[3]
    if raw_date:
      # if it's already a datetime obj, format it. if it's a string, show the first 10 char
      date_str = row[3].strftime("%Y-%m-%d") if hasattr(raw_date, "strftime") else str(raw_date)[:10]
    else: 
      date_str = "N/A"
    
    print(f"{short_sha:<12} | {repo:<20} | {date_str:<12} | {short_msg:<30}")
  
  cursor.execute("SELECT COUNT(*) FROM commits;")
  total_commits = cursor.fetchone()[0]
  print(f"Total Commits Stored: {total_commits}\n")

  cursor.close()
  conn.close()
if __name__ == "__main__":
  view_repositories()
  #view_commits()