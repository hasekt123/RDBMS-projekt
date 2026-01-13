from database import db

class TableGateway:
    def __init__(self, table_name):
        self.table = table_name

    def fetch_all(self):
        cursor = db.get_cursor()
        query = f"SELECT * FROM {self.table}"
        cursor.execute(query)
        return cursor.fetchall()

class ZakaznikGateway(TableGateway):
    def __init__(self):
        super().__init__('zakaznici')

    def insert(self, jmeno, email):
        try:
            cursor = db.get_cursor()
            cursor.execute("INSERT INTO zakaznici (jmeno, email) VALUES (?, ?)", (jmeno, email))
            db.commit()
            print(f"Zákazník {jmeno} vložen.")
        except Exception as e:
            print(f"Chyba při vkládání zákazníka: {e}")

class ProduktGateway(TableGateway):
    def __init__(self):
        super().__init__('produkty')

    def get_active(self):
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM view_aktivni_produkty")
        return cursor.fetchall()

class ObjednavkaGateway(TableGateway):
    def __init__(self):
        super().__init__('objednavky')

    def vytvorit_objednavku(self, zakaznik_id, polozky_list):

        cursor = db.get_cursor()
        try:
            cursor.execute("INSERT INTO objednavky (zakaznik_id, stav) VALUES (?, ?)", (zakaznik_id, 'nova'))
            
            cursor.execute("SELECT @@IDENTITY")
            row = cursor.fetchone()
            if not row:
                raise Exception("Nepodařilo se získat ID objednávky.")
            objednavka_id = int(row[0])

            for item in polozky_list:
                prod_id, pocet, cena = item
                cursor.execute(
                    "INSERT INTO polozky_objednavky (objednavka_id, produkt_id, pocet_kusu, cena_za_kus) VALUES (?, ?, ?, ?)",
                    (objednavka_id, prod_id, pocet, cena)
                )

            db.commit()
            print(f"Objednávka č. {objednavka_id} byla úspěšně vytvořena!")

        except Exception as e:
            db.rollback()
            print(f"CHYBA TRANSAKCE: Objednávka nebyla vytvořena. Důvod: {e}")

    def report_prehled(self):
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM view_prehled_objednavek")
        return cursor.fetchall()