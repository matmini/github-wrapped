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