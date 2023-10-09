import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert


def data_load():
    # Define your database connection URL
    db_url = 'postgresql://connection_string'

    # Create a SQLAlchemy engine
    engine = create_engine(db_url)

    # Load CSV files into DataFrames
    deposit_df = pd.read_csv('../tmp/deposit_sample_data.csv')
    withdrawal_df = pd.read_csv('../tmp/withdrawals_sample_data.csv')
    event_df = pd.read_csv('../tmp/event_sample_data.csv')
    user_df = pd.read_csv('../tmp/user_id_sample_data.csv')

    # Populate the user dimension table
    user_df.to_sql('dim_user', engine, if_exists='append', index=False)

    # Populate the events dimension table    
    event_df.to_sql('dim_event', engine, if_exists='append', index=False, chunksize=1000)

    # Add the transaction_type column to withdrawal and deposit df
    withdrawal_df['transaction_type'] = 'withdrawal'
    deposit_df['transaction_type'] = 'deposit'

    # Populate the transactions fact table
    transactions = pd.concat([deposit_df, withdrawal_df])
    transactions.to_sql(
        'fact_transactions',
        engine,
        if_exists='append',
        index=False,
        chunksize=10000)

    # Close DB connection
    engine.dispose()
    
data_load()