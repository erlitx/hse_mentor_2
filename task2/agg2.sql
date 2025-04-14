WITH txn_logs AS (
    SELECT
        t.user_id,
        t.transaction_id,
        COUNT(l.log_id) AS log_count
    FROM transactions_v2 t
    LEFT JOIN logs_v2 l ON t.transaction_id = l.transaction_id
    GROUP BY t.user_id, t.transaction_id
)
SELECT
    user_id,
    COUNT(*) AS txn_count,
    SUM(log_count) AS total_logs,
    AVG(log_count) AS avg_logs_per_txn
FROM txn_logs
GROUP BY user_id
ORDER BY avg_logs_per_txn DESC
LIMIT 10;
