import traceback, sys
import time
import logging
import requests
import psycopg2
import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read('CONFIG.ini')

def database_connection():
    try:
        conn = psycopg2.connect(f"""dbname={CONFIG['myPostgresDB']['dbname']} user={CONFIG['myPostgresDB']['user']} host={CONFIG['myPostgresDB']['host']} password={CONFIG['myPostgresDB']['password']} port={CONFIG['myPostgresDB']['port']}""")
        conn.autocommit = True
        cursor = conn.cursor()
        print('-----------------------------------------------')
        print("Connected to database...")
        print()
        return cursor
    except Exception as e:
        get_trace_and_log(e)
        print("Cannot connect to database...")
        
