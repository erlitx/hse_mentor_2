WITH good_txns AS (
  SELECT *
  FROM transactions_v2
  WHERE currency IN ('USD', 'EUR', 'RUB')
),
txn_logs AS (
  SELECT 
    t.user_id,
    t.transaction_id,
    t.amount,
    l.log_id
  FROM good_txns t
  LEFT JOIN logs_v2 l ON t.transaction_id = l.transaction_id
),
agg AS (
  SELECT
    user_id,
    COUNT(DISTINCT transaction_id) AS txn_count,
    SUM(amount) AS total_amount,
    COUNT(log_id) AS total_logs
  FROM txn_logs
  GROUP BY user_id
)
SELECT *
FROM agg
ORDER BY total_amount DESC
LIMIT 5;
