import psycopg2
import pandas as pd
import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read('CONFIG.ini')

def fetch_data(query):
    """(query: str) -> str

    Takes in a query, connects to the database and returns the result."""
    result = pd.read_sql(
        sql=query,
        con=psycopg2.connect(
            f"""dbname={CONFIG['myPostgresDB']['dbname']} user={CONFIG['myPostgresDB']['user']} host={CONFIG['myPostgresDB']['host']} password={CONFIG['myPostgresDB']['password']} port={CONFIG['myPostgresDB']['port']}""")
    )
    return result
    
