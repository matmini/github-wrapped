-- name: github_username
SELECT username 
FROM repositories 
WHERE username IS NOT NULL 
LIMIT 1;

-- name: total_commits
SELECT COUNT(*) as total_count FROM commits;

-- name: total_repos 
SELECT COUNT(*) as total_count FROM repositories;

-- name: busiest_day 
SELECT 
  EXTRACT(DOW FROM author_date) as day_num, 
  COUNT(*) as commit_count 
FROM commits 
GROUP BY day_num 
ORDER BY commit_count DESC 
LIMIT 1; 

-- name: favorite_word 
SELECT
  word,
  COUNT(*) as word_count 
FROM (
  SELECT regexp_split_to_table(lower(message), '\s+') as word
  FROM commits
) words 
WHERE length(word) > 3 AND word NOT IN ('with', 'this', 'that', 'from', 'your', 'merge', 'branch')
GROUP BY word
ORDER BY word_count DESC
LIMIT 1; 

-- name: top_language
SELECT  
  language,
  COUNT(*) as repo_count
FROM repositories 
WHERE language IS NOT NULL
GROUP BY language
ORDER BY repo_count DESC
LIMIT 1;

-- name: busiest_hour 
SELECT 
  EXTRACT(HOUR FROM author_date AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Manila') as commit_hour,
  COUNT(*) as commit_count 
FROM commits 
GROUP BY commit_hour
ORDER BY commit_count DESC 
LIMIT 1

-- name: longest_streak 
WITH unique_days AS (
  SELECT DISTINCT DATE_TRUNC('day', author_date) as commit_date
  FROM commits
), 
indexed_days AS (
  -- Asign a sequential row number sorted by date 
  SELECT 
    commit_date,
    ROW_NUMBER() OVER (ORDER BY commit_date) as row_num 
  FROM unique_days
),
streaks AS (
  -- Subtract row_num from commit_date to find groups of consecutive days
  SELECT 
    commit_date - (row_num * INTERVAL '1 day') as streak_group,
    COUNT(*) as streak_length 
  FROM indexed_days
  GROUP BY streak_group 
)
-- Grab the longest consecutive block 
SELECT streak_length
FROM streaks 
ORDER BY streak_length DESC 
LIMIT 1;

-- name: top_commit_hours 
SELECT 
  EXTRACT(HOUR FROM author_date AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Manila') as commit_hour,
  COUNT(*) as commit_count 
FROM commits 
GROUP BY commit_hour 
ORDER BY commit_count DESC 
LIMIT 5; 