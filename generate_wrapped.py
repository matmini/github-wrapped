import os 
import psycopg 
from dotenv import load_dotenv

load_dotenv() 

def get_db_connection():
  return psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
  )

def load_sql_queries(filepath="queries.sql"):
  """Reads a .sql file and splits queries based on '-- name:' markers."""
  queries = {}
  current_name = None 
  current_lines = [] 

  with open(filepath, "r") as f: 
    for line in f: 
      if line.startswith("-- name:"):
        # Save previous query if it exists 
        if current_name: 
          queries[current_name] = "".join(current_lines).strip()
        current_name = line.replace("-- name:", "").strip()
        current_lines = []
      elif current_name: 
        current_lines.append(line)
    
    # Catch the final query in the file 
    if current_name: 
      queries[current_name] = "".join(current_lines).strip()
  return queries

def calculate_wrapped_stats(): 
  # Load the external SQL statements 
  sql = load_sql_queries()

  # Establist database connection
  conn = get_db_connection()
  cursor = conn.cursor() 

  print("\n-- YOUR GITHUB WRAPPED ANALYTICS --") 
  print("=" * 45)

  # STAT 1: Your Busiest Coding Day of the Week 
  # (Postgresql 'dow' extracts Day of Week: 0 = Sunday, 1 = Monday, etc.)
  cursor.execute(sql["busiest_day"])
  busiest_day = cursor.fetchone() 

  days_map = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
  }

  if busiest_day and busiest_day[0] is not None:
    day_index = int(busiest_day[0])
    day_name = days_map[day_index]
    commit_count = busiest_day[1]
    print(f"Busiest Day: You do your best word on {day_name}s! ({commit_count} commits)")
  else: 
    print("Busiest dDay: Not enough commit history found yet.")

  # STAT 2: Most Common Word in Your Commit Message 
  cursor.execute(sql["favorite_word"])
  favorite_word_result = cursor.fetchone()

  if favorite_word_result:
    favorite_word = favorite_word_result[0]
    word_count = favorite_word_result[1]
    print(f"Favorite Code Word: You loved typing '{favorite_word} ({word_count} times)!")
  else :
    print("Favorite Code Word: No commit messages found to analyze.")

  # STAT 3: Favorite Language 
  cursor.execute(sql["top_language"]) 
  top_language_result = cursor.fetchone() 
  if top_language_result is not None: 
    top_language = top_language_result[0]
    numOfRepos = top_language_result[1]
    print(f"Top Language: Your used {top_language} in {numOfRepos} repos!")
  else: 
    print(f"Top Language: Ooops! There's no top language.")
if __name__ == "__main__":
  calculate_wrapped_stats() 

