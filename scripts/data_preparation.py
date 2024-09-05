import pandas as pd
from database import get_connection

def load_data(table_name):
    connection = get_connection()
    if connection is not None:
        query = f'SELECT * FROM {table_name}'
        data = pd.read_sql(query, connection)
        connection.close()
        return data
    else:
        raise Exception("Failed to connect to the database.")

def clean_data(data):
    data = data.dropna()  # Drop rows with missing values
    return data
