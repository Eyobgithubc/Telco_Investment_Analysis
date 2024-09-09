import sys
import os
import pandas as pd
import numpy as np
sys.path.append(r'C:/Users/teeyob/Telco_Investment_Analysis/src')

from database import get_connection

def load_data(xdr_data):
    engine = get_connection()
    if engine is not None:
        query = f'SELECT * FROM xdr_data'
        data = pd.read_sql(query, engine)
        return data
    else:
        raise Exception("Failed to connect to the database.")

def clean_data(data):
    # Check that data is a DataFrame
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input data should be a pandas DataFrame.")
    
    # Drop duplicates
    data = data.drop_duplicates()
    
    # Fill missing values
    data = data.fillna(0)

    def detect_outliers(df, columns):
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        return df

    # Detect and remove outliers
    numerical_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    if numerical_columns:
        data = detect_outliers(data, numerical_columns)
    else:
        print("No numerical columns found for outlier detection.")
    
    return data

