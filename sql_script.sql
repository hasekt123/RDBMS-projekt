/*
=============================================================
PROJEKT: Eshop Manažer (Python + MSSQL)
AUTOR:   Zomáš Oliver hašek C4c
EMAIL:   tomik.hasek@gmail.com
DATUM:   4.1
POPIS:   Skript pro vytvoøení databáze (DDL) a naplnìní
         testovacími daty (DML). Celý proces je chránìn
         transakcí.
=============================================================
*/

USE [master];
GO

IF EXISTS (SELECT name FROM sys.databases WHERE name = N'eshop_projekt')
BEGIN
    ALTER DATABASE [eshop_projekt] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE [eshop_projekt];
END
GO

CREATE DATABASE [eshop_projekt];
GO

USE [eshop_projekt];
GO

PRINT 'Zahajuji vytváøení struktury...';

BEGIN TRANSACTION;

BEGIN TRY

    CREATE TABLE [dbo].[zakaznici](
        [id] [int] IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [jmeno] [nvarchar](100) NOT NULL,
        [email] [nvarchar](100) NOT NULL UNIQUE
    );

    CREATE TABLE [dbo].[kategorie](
        [id] [int] IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [nazev] [nvarchar](50) NOT NULL
    );

    CREATE TABLE [dbo].[produkty](
        [id] [int] IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [nazev] [nvarchar](100) NOT NULL,
        [cena] [float] NOT NULL,
        [aktivni] [bit] NULL DEFAULT 1,
        [kategorie_id] [int] NULL,
        FOREIGN KEY ([kategorie_id]) REFERENCES [dbo].[kategorie] ([id])
    );

    CREATE TABLE [dbo].[objednavky](
        [id] [int] IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [zakaznik_id] [int] NOT NULL,
        [datum_vytvoreni] [datetime] NULL DEFAULT GETDATE(),
        [stav] [varchar](20) NOT NULL CHECK ([stav] IN ('nova', 'zaplacena', 'odeslana', 'zrusena')),
        FOREIGN KEY ([zakaznik_id]) REFERENCES [dbo].[zakaznici] ([id])
    );

    CREATE TABLE [dbo].[polozky_objednavky](
        [objednavka_id] [int] NOT NULL,
        [produkt_id] [int] NOT NULL,
        [pocet_kusu] [int] NOT NULL,
        [cena_za_kus] [float] NOT NULL,
        PRIMARY KEY ([objednavka_id], [produkt_id]),
        FOREIGN KEY ([objednavka_id]) REFERENCES [dbo].[objednavky] ([id]),
        FOREIGN KEY ([produkt_id]) REFERENCES [dbo].[produkty] ([id])
    );


    EXEC('CREATE VIEW [dbo].[view_prehled_objednavek] AS
          SELECT o.id, o.datum_vytvoreni, o.stav, z.jmeno AS zakaznik, z.email
          FROM objednavky o JOIN zakaznici z ON o.zakaznik_id = z.id');

    EXEC('CREATE VIEW [dbo].[view_aktivni_produkty] AS
          SELECT p.id, p.nazev, p.cena, k.nazev AS kategorie
          FROM produkty p JOIN kategorie k ON p.kategorie_id = k.id
          WHERE p.aktivni = 1');

    INSERT INTO kategorie (nazev) VALUES ('Elektronika'), ('Obleceni');
    
    INSERT INTO produkty (nazev, cena, aktivni, kategorie_id) VALUES 
    ('Herni Notebook', 25000, 1, 1), 
    ('Bezdrátová myš', 500, 1, 1),
    ('Trièko Python', 350, 1, 2);

    INSERT INTO zakaznici (jmeno, email) VALUES 
    ('Jan Novák', 'jan@test.cz'),
    ('Petr Svoboda', 'petr@test.cz');

    INSERT INTO objednavky (zakaznik_id, stav) VALUES (1, 'nova');
    INSERT INTO polozky_objednavky (objednavka_id, produkt_id, pocet_kusu, cena_za_kus) VALUES 
    (1, 1, 1, 25000),
    (1, 2, 2, 500);

    COMMIT TRANSACTION;
    PRINT 'HOTOVO! Databáze byla úspìšnì vytvoøena a naplnìna daty.';

END TRY
BEGIN CATCH
    ROLLBACK TRANSACTION;
    PRINT '!!! KRITICKÁ CHYBA PØI VYTVÁØENÍ DATABÁZE !!!';
    PRINT 'Chyba: ' + ERROR_MESSAGE();
END CATCH;
GO