CREATE TABLE transactions_v2 (
    transaction_id UInt32,
    user_id UInt32,
    transaction_date Date,
    amount Float32,
    currency String,
    is_fraud UInt8
) ENGINE = MergeTree()
ORDER BY (transaction_date, transaction_id);


CREATE TABLE logs_v2 (
    log_id UInt32,
    transaction_id UInt32,
    category String,
    log_time DateTime
) ENGINE = MergeTree()
ORDER BY (transaction_id, log_time);
