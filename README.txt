NÁZEV: Eshop Manažer
AUTOR: Tomáš Oliver Hašek C4c
TYP: Zadání D1 (Table Gateway)

JAK ZPROVOZNIT PROJEKT (Návod pro školní PC):

1. Databáze (SQL Script):
   - Otevřete SQL Server Management Studio (SSMS).
   - Přihlaste se
   - Vytvořte databázi eshop_projekt
   - Otevřete soubor "sql_script.sql" z hlavní složky projektu.
   - Spusťte ho tlačítkem Execute (F5). Musí napsat "HOTOVO".

2. Konfigurace Pythonu:
   - Aplikace je nastavena na SQL Authentication (Login: sa, Heslo: student).
   - Otevřete soubor "src/config.py".
   - Zkontrolujte/Upravte řádek DB_SERVER = ... podle čísla vašeho školního pc.
     (Číslo pc vidíte v přihlašovacím okně SSMS).

3. (Možná bude potřeba stáhnout python z internetu, to poznáte v pycharmu. Nevím proč ale ke dni 13.1. mi na školních pc nefungoval.)

4. Spuštění:

Přes vývojové prostředí:
   - Otevřete projekt v pycharm nebo jiném programu.
   - Stáhněte package pyodbc y z database.py
   - Program spusťte a užívejte dle libosti :-)-

Bez vývojového prostředí:
   - Přejděte do složky src v projektu:
   - Cestu k projektu (ve file exploreru) nahraďte slovem cmd. příklad: C:\Users\hasek\Downloads\EshopProjekt
   - Nainstalujte knihovnu (přepínač --user obchází zákaz instalace):
     pip install --user pyodbc
   - Spusťte program:
     python main.py

ŘEŠENÍ PROBLÉMŮ:
- Chyba "Login failed for user 'sa'": Zkontrolujte, zda školní server opravdu používá heslo "student". Pokud ne, upravte config.py.
- Chyba "Server not found": Máte špatný název serveru v config.py.
