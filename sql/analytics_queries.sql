-- Window & analytics queries

-- 1) User recency rank
SELECT
  user_id, item_id, action, created_at,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS recency_rank
FROM transactions
WHERE action IN ('click','purchase');

-- 2) Cumulative interactions per user
SELECT
  user_id,
  created_at,
  COUNT(*) OVER (PARTITION BY user_id ORDER BY created_at
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_interactions
FROM transactions;

-- 3) Average time between purchases
SELECT
  user_id,
  AVG(TIMESTAMPDIFF(SECOND, prev_ts, created_at)) AS avg_seconds_between_purchases
FROM (
  SELECT
    user_id, created_at,
    LAG(created_at) OVER (PARTITION BY user_id ORDER BY created_at) AS prev_ts
  FROM transactions
  WHERE action = 'purchase'
) t
WHERE prev_ts IS NOT NULL
GROUP BY user_id;

-- 4) Item conversion rate (click -> purchase)
WITH item_actions AS (
  SELECT
    item_id,
    SUM(action='click')     AS clicks,
    SUM(action='purchase')  AS purchases
  FROM transactions
  GROUP BY item_id
)
SELECT
  item_id, clicks, purchases,
  CASE WHEN clicks > 0 THEN purchases / clicks ELSE 0 END AS conversion_rate
FROM item_actions;
