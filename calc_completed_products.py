import psycopg2
# from static_data import stores_and_modifiers
# from get_data_general import final_list_sell
# from get_data_general import final_list_buy
from gen_utils import get_trace_and_log


class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='a' user='b' host='c' password='d' port='e'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print('Connected to database...\n')
        except Exception as e:
            get_trace_and_log(e)
            print('Cannot connect to database...')

    def insert_stats(self, value):
        if value is 'Alpha':
            # Add try/catch loop so we don't just hit a full stop when we error out?
            try:
                self.cursor.execute("""
                INSERT INTO completed_products_stats(completed_product_nick, completed_product_avg, completed_product_min, completed_product_max)
                SELECT completed_product_nick, avg(completed_product_prices), min(completed_product_prices), max(completed_product_prices)
                FROM completed_products
                WHERE completed_product_nick IN ('Alpha Black Lotus', 'Alpha Mox Sapphire', 'Alpha Mox Jet', 'Alpha Mox Pearl', 'Alpha Mox Ruby', 'Alpha Mox Emerald', 'Alpha Timetwister', 'Alpha Ancestral Recall', 'Alpha Time Walk')
                GROUP BY completed_product_nick""")
            except Exception as e:
                get_trace_and_log(e)
                pass
        else:
            # Add try/catch loop so we don't just hit a full stop when we error out?
            try:
                self.cursor.execute(f"""
                INSERT INTO completed_products_stats(completed_product_nick, completed_product_avg, completed_product_min, completed_product_max)
                SELECT completed_product_nick, avg(completed_product_prices), min(completed_product_prices), max(completed_product_prices)
                FROM completed_products
                WHERE completed_product_nick IN ('{value} Black Lotus MTG', '{value} Mox Sapphire', '{value} Mox Jet', '{value} Mox Pearl', '{value} Mox Ruby', '{value} Mox Emerald', '{value} Timetwister', '{value} Ancestral Recall', '{value} Time Walk')
                GROUP BY completed_product_nick""")
            except Exception as e:
                get_trace_and_log(e)
                pass

    def insert_index(self, value):
        if value is 'Alpha':
            # Add try/catch loop so we don't just hit a full stop when we error out?
            try:
                self.cursor.execute(f"""
                INSERT INTO completed_products_index(completed_product_set_name, completed_product_set_id, completed_product_index_avg, completed_product_index_min, completed_product_index_max)
                SELECT '{value}', '1', sum(completed_product_avg), sum(completed_product_min), sum(completed_product_max)
                FROM completed_products_stats
                WHERE completed_product_nick IN ('{value} Black Lotus', '{value} Mox Sapphire', '{value} Mox Jet', '{value} Mox Pearl', '{value} Mox Ruby', '{value} Mox Emerald', '{value} Timetwister', '{value} Ancestral Recall', '{value} Time Walk')
                """)
            except Exception as e:
                get_trace_and_log(e)
        elif value is 'Beta':
            try:
                self.cursor.execute(f"""
                INSERT INTO completed_products_index(completed_product_set_name, completed_product_set_id, completed_product_index_avg, completed_product_index_min, completed_product_index_max)
                SELECT '{value}', '2', sum(completed_product_avg), sum(completed_product_min), sum(completed_product_max)
                FROM completed_products_stats
                WHERE completed_product_nick IN ('{value} Black Lotus MTG', '{value} Mox Sapphire', '{value} Mox Jet', '{value} Mox Pearl', '{value} Mox Ruby', '{value} Mox Emerald', '{value} Timetwister', '{value} Ancestral Recall', '{value} Time Walk')
                """)
            except Exception as e:
                # print('Duplicate values, moving forward...\n')
               get_trace_and_log(e)
        else:
            try:
                self.cursor.execute(f"""
                INSERT INTO completed_products_index(completed_product_set_name, completed_product_set_id, completed_product_index_avg, completed_product_index_min, completed_product_index_max)
                SELECT '{value}', '3', sum(completed_product_avg), sum(completed_product_min), sum(completed_product_max)
                FROM completed_products_stats
                WHERE completed_product_nick IN ('{value} Black Lotus MTG', '{value} Mox Sapphire', '{value} Mox Jet', '{value} Mox Pearl', '{value} Mox Ruby', '{value} Mox Emerald', '{value} Timetwister', '{value} Ancestral Recall', '{value} Time Walk')
                """)
            except Exception as e:
                get_trace_and_log(e)

if __name__ == '__main__':
    database_connection = DatabaseConnection()
    values = ['Alpha', 'Beta', 'Unlimited']
    for value in values:
        print(f'Inserting {value} data points...')
        database_connection.insert_stats(value)
        database_connection.insert_index(value)
    print()
    print('(<*.*<) DATABASE HAS BEEN |P I P E D| (>*.*>)')
