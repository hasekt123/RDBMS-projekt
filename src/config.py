# config.py
# Nastavení aplikace a připojení k databázi

# Zde nastavte název serveru (např. 'PC123).
DB_SERVER = r'pc777'

DB_NAME = 'eshop_projekt'

# Nastavení pro SQL Authentication (školní login: sa / student)
CONNECTION_STRING = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={DB_SERVER};'
    f'DATABASE={DB_NAME};'
    f'UID=sa;'             # Uživatelské jméno
    f'PWD=student;'        # Heslo
    f'Encrypt=no;'
)

# Název souboru pro import dat
IMPORT_FILE_PATH = '../data/zakaznici.csv'