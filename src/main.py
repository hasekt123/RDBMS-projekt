import sys
import csv
import os
from database import db
from gateways import ZakaznikGateway, ProduktGateway, ObjednavkaGateway
import config

def zobrazit_menu():
    print("\n" + "="*30)
    print("      ESHOP MANAŽER v1.0")
    print("="*30)
    print("1. Zobrazit aktivní produkty (Ceník)")
    print("2. Zobrazit zákazníky")
    print("3. Přidat nového zákazníka")
    print("4. Vytvořit objednávku (Transakce)")
    print("5. Report objednávek (View)")
    print("6. Import zákazníků z CSV")
    print("0. Konec")
    print("="*30)

def import_z_csv():
    cesta = config.IMPORT_FILE_PATH
    if not os.path.exists(cesta):
        print(f"Chyba: Soubor {cesta} neexistuje.")
        return

    print("Importuji data...")
    gw = ZakaznikGateway()
    try:
        with open(cesta, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            pocet = 0
            for row in reader:
                if len(row) >= 2:
                    gw.insert(row[0], row[1])
                    pocet += 1
            print(f"Import dokončen. Vloženo {pocet} zákazníků.")
    except Exception as e:
        print(f"Chyba při importu: {e}")

def main():
    db.connect()
    
    zg = ZakaznikGateway()
    pg = ProduktGateway()
    og = ObjednavkaGateway()

    while True:
        zobrazit_menu()
        volba = input("Vyberte akci: ")

        if volba == '1':
            produkty = pg.get_active()
            print("\n--- AKTIVNÍ PRODUKTY ---")
            for p in produkty:
                # p[0]=nazev, p[1]=cena, p[2]=kategorie (z View)
                print(f"Produkt: {p[0]} | Cena: {p[1]} Kč | Kat: {p[2]}")

        elif volba == '2':
            zakaznici = zg.fetch_all()
            print("\n--- SEZNAM ZÁKAZNÍKŮ ---")
            for z in zakaznici:
                print(f"ID: {z[0]}, Jméno: {z[1]}, Email: {z[2]}")

        elif volba == '3':
            jm = input("Zadej jméno: ")
            em = input("Zadej email: ")
            if jm and em:
                zg.insert(jm, em)
            else:
                print("Chyba: Údaje nesmí být prázdné.")

        elif volba == '4':
            try:
                id_zak = input("Zadej ID zákazníka: ")
                kosik = []
                while True:
                    print("\nPřidat položku do objednávky?")
                    id_prod = input("ID Produktu (nebo Enter pro konec): ")
                    if not id_prod: break
                    ks = input("Počet kusů: ")
                    cena = input("Aktuální cena za kus: ")
                    kosik.append((int(id_prod), int(ks), float(cena)))
                
                if kosik:
                    og.vytvorit_objednavku(int(id_zak), kosik)
                else:
                    print("Košík je prázdný, objednávka zrušena.")
            except ValueError:
                print("Chyba: Musíte zadávat čísla!")

        elif volba == '5':
            report = og.report_prehled()
            print("\n--- REPORT OBJEDNÁVEK ---")
            for r in report:
                print(f"Objednávka #{r[0]} | Datum: {r[1]} | Stav: {r[2]} | Zákazník: {r[3]}")

        elif volba == '6':
            import_z_csv()

        elif volba == '0':
            print("Nashledanou.")
            break
        else:
            print("Neplatná volba, zkuste to znovu.")

    db.close()

if __name__ == "__main__":
    main()