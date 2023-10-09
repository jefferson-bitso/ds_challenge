
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS dim_event;
DROP TABLE IF EXISTS dim_user;

CREATE TABLE dim_user (
    user_id TEXT PRIMARY KEY
);

CREATE TABLE dim_event (
    id BIGINT PRIMARY KEY,
    event_timestamp TIMESTAMP,
    event_date DATE GENERATED ALWAYS AS (event_timestamp::date) STORED,
    user_id TEXT REFERENCES dim_user(user_id),
    event_name TEXT
    );

CREATE TABLE fact_transactions (
    ds_id BIGSERIAL PRIMARY KEY,
    id BIGINT,
    transaction_type TEXT,
    event_timestamp TIMESTAMP,
    event_date DATE GENERATED ALWAYS AS (event_timestamp::date) STORED,
    user_id TEXT REFERENCES dim_user(user_id),
    amount FLOAT,
    currency TEXT,
    tx_status TEXT,
    interface text
);

CREATE INDEX CONCURRENTLY ON fact_transactions (user_id, transaction_type);
CREATE INDEX CONCURRENTLY ON fact_transactions (event_date);
CREATE INDEX CONCURRENTLY ON dim_event (user_id, event_timestamp);
CREATE INDEX CONCURRENTLY ON dim_user (user_id);
