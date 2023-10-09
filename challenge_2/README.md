# DS Challenge 2

The database modeling used a pseudo star-schema which a big `transaction` fact table was created to accomodate all deposits and withdrawals.
That way, we avoid unecessary joins when gathering transactions data.

The output of `fact_transactions` table (`fact_transactions_limited.csv.zip`) had to be limited to 1M rows due to the file limitation size on Github.