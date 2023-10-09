--Chalenge 2 - Queries

--How many users were active on a given day (they made a deposit or withdrawal)
SELECT COUNT(DISTINCT user_id) 
FROM fact_transactions WHERE event_date = '2020-10-10';

--Identify users haven't made a deposit
SELECT u.user_id, f.user_id 
FROM dim_user u
LEFT JOIN fact_transactions f ON f.user_id = u.user_id AND f.transaction_type = 'deposit'
WHERE f.user_id IS NULL ;

--Identify on a given day which users have made more than 5 deposits historically
SELECT user_id, event_date, COUNT(*) AS "deposits_count"
FROM fact_transactions
WHERE event_date = '2020-06-03'
GROUP BY user_id, event_date
HAVING COUNT(*) > 5
ORDER BY 2;

--When was the last time a user a user made a login
SELECT user_id, max(event_timestamp) AS "last_login"
FROM dim_event
WHERE event_name IN ('login','2falogin','login_api')
AND user_id = '2270fa1dcbebe770b3b8158dc8ff3265'
GROUP BY user_id;

--How many times a user has made a login between two dates
SELECT user_id, COUNT(*) as "login_count"
FROM dim_event
WHERE event_name = 'login'
AND event_date BETWEEN '2021-05-10' AND '2023-10-10'
AND user_id = '2270fa1dcbebe770b3b8158dc8ff3265'
GROUP BY user_id;

--Number of unique currencies deposited on a given day
SELECT currency, COUNT(*) AS "count_deposits"
FROM fact_transactions
WHERE transaction_type = 'deposit'
AND event_date = '2020-01-02'
GROUP BY 1;

--Number of unique currencies withdrew on a given day
SELECT currency, COUNT(*) AS "count_withdrawals"
FROM fact_transactions
WHERE transaction_type = 'withdrawal'
AND event_date = '2020-06-02'
GROUP BY 1;

--Total amount deposited of a given currency on a given day
SELECT currency, SUM(amount) 
FROM fact_transactions
WHERE transaction_type = 'deposit'
AND event_date = '2020-06-02'
GROUP BY 1;

