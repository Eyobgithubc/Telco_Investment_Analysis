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

import pandas as pd
import numpy as np

def clean_data(data):
    
    data = data.drop_duplicates()
    
    
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
    
   
    numerical_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    

    data = detect_outliers(data, numerical_columns)
    
    return data

