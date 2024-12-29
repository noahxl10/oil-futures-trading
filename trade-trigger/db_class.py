import psycopg2 as ps
import configparser


class Database:

    def __init__(self, app:str, config_path:str):
        self.app = app
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.conn = ps.connect(
            host=self.config['DATABASE']['HOST'],
            database=self.config['DATABASE']['NAME'],
            user=self.config['DATABASE']['USERNAME'],
            password=self.config['DATABASE']['PASSWORD'],
            port=self.config['DATABASE']['PORT']
            )
        self.cur = self.conn.cursor()
        self.cur.execute("ROLLBACK")
        self.conn.commit()

    def delete_migration(self, table:str):
        print(f'''DELETE FROM {table} WHERE app = '{self.app}';''')
        try:
            self.cur.execute(f'''DELETE FROM {table} WHERE app = '{self.app}';''')
            self.conn.commit()
        except ps.errors.UndefinedTable:
            print(f'\nFor db: migrations table for {self.app} does not exist\n')

    def drop(self, table:str):
        print(f"DROP TABLE IF EXISTS {table};")
        try:
            self.cur.execute(f'DROP TABLE IF EXISTS {table};')
            self.conn.commit()
        except ps.errors.InFailedSqlTransaction:
            print(f'\nDrop table failed for {table}\n')


    def query(self, query_str:str):
        self.cur.execute(query_str)
        self.conn.commit()
        
    def close(self):
        self.cur.close()
        self.conn.close()