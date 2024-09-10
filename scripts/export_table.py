import sys
import os
import pandas as pd
import numpy as np
sys.path.append(r'C:/Users/teeyob/Telco_Investment_Analysis/src')

from database import get_connection

def export_to_Postgres(df, table_name):
   
   
    engine = get_connection()
    
    if engine is not None:
        try:
           
            df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            print(f"Table '{table_name}' has been successfully exported to the PostgreSQL database.")
        except Exception as e:
            print("Error exporting data:", e)
    else:
        print("Failed to establish a database connection.")