WITH txn_with_logs AS (
  SELECT
    t.transaction_id,
    t.transaction_date,
    COUNT(l.log_id) AS log_count
  FROM transactions_v2 t
  LEFT JOIN logs_v2 l ON t.transaction_id = l.transaction_id
  GROUP BY t.transaction_id, t.transaction_date
),
avg_logs_per_day AS (
  SELECT *,
         AVG(log_count) OVER (PARTITION BY transaction_date) AS avg_logs_for_day
  FROM txn_with_logs
)
SELECT *
FROM avg_logs_per_day
WHERE log_count > avg_logs_for_day * 2
ORDER BY transaction_date, log_count DESC;
