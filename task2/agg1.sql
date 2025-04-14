SELECT
    transaction_date,
    COUNT() AS fraud_count,
    SUM(amount) AS total_fraud_amount,
    AVG(amount) AS avg_fraud_amount
FROM transactions_v2
WHERE is_fraud = 1
GROUP BY transaction_date
ORDER BY fraud_count DESC
LIMIT 5;
