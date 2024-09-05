import psycopg2
from psycopg2 import OperationalError

def get_connection():
    hostname='localhost'
    database='telecom_db'
    username='postgres'
    pwd='2525'
    port_id='5432'
   
    try:
        connection = psycopg2.connect(
            
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id
            
        )
        
        print("Connection successful")
        return connection
    except OperationalError as e:
        print("OperationalError:", e)
    except Exception as e:
        print("Error connecting to the database:", e)
    return None
