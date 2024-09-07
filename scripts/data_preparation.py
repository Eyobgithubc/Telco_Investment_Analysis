import sys
import os
import pandas as pd
import numpy as np
sys.path.append(r'C:/Users/teeyob/Telco_Investment_Analysis/src')

from database import get_connection

def load_data(table_name):
    engine = get_connection()
    if engine is not None:
        query = f'SELECT * FROM xdr_data'
        data = pd.read_sql(query, engine)
        return data
    else:
        raise Exception("Failed to connect to the database.")

def clean_data(data):
    # Remove duplicates
    data = data.drop_duplicates()
    # Fill missing values with zero
    data = data.fillna(0)

    # Function to detect and remove outliers based on IQR
    def detect_outliers(df, columns):
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        return df

    # Get numerical columns to check for outliers
    numerical_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    # Clean data by removing outliers
    data = detect_outliers(data, numerical_columns)

    return data

# Example usage:
try:
    data = load_data('your_table_name')
    clean_data = clean_data(data)
    print(clean_data.head())
except Exception as e:
    print(f"Error: {e}")
