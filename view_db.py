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
  cursor.execute("SELECT id, name, language, stars FROM repositories ORDER BY stars DESC;")
  rows = cursor.fetchall() 

  print("\n --- DATABASE ENTRIES (Sorted by Stars) --- ")
  print(f"{'ID':<5} | {'Repository Name':<30} | {'Language':<15} | {'Stars':<5} ")
  print("-"* 65) 

  for row in rows:
    print(f"{row[0]:<5} | {row[1]:<30} | {row[2]:<15} | {row[3]:<5}")
        
  print(f"---------------------------------------------\nTotal rows found: {len(rows)}\n")
    
  cursor.close()
  conn.close()

if __name__ == "__main__":
  view_repositories()