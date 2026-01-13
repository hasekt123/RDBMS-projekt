import pyodbc
import config

class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            if not self.conn:
                print(f"Připojuji se k {config.DB_SERVER}...")
                self.conn = pyodbc.connect(config.CONNECTION_STRING)
                print("Připojení úspěšné.")
        except pyodbc.Error as e:
            print(f"!!! CHYBA PŘIPOJENÍ K DATABÁZI !!!")
            print(f"Detail: {e}")
            print("Zkontrolujte název serveru v config.py a zda běží SQL Server.")
            exit()

    def close(self):
        if self.conn:
            self.conn.close()

    def get_cursor(self):
        if not self.conn:
            self.connect()
        return self.conn.cursor()

    def commit(self):
        if self.conn:
            self.conn.commit()
    
    def rollback(self):
        if self.conn:
            self.conn.rollback()

db = Database()