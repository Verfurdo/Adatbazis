# Kemence Panelhőmérséklet Adatbázis Projekt

Egy Streamlit alapú Python alkalmazás, amivel CSV fájlokból ipari kemence adatokat lehet adatbázisba tölteni, tisztítani, böngészni és különféle SQL-lekérdezésekkel elemezni.
A rendszer alkalmas gyártási adagok és szenzoros hűtőpanel mérések kezelésére, vizsgálatára.

## Tartalom

- [Előfeltételek](#elofeltetelek)
- [Telepítés](#telepites)
- [Használat](#hasznalat)
- [Fájlok magyarázata](#fajlok-magyarazata)
- [Fő funkciók](#funkciok)
- [Működés](#mukodes)
- [Közreműködők](#kozremukodok)

## Előfeltételek

Követelmény modulok:
-	streamlit
-   pandas
-	os
-	sqlite3

A data/ mappában legyenek:

-   Adagok.csv
-   Hűtőpanelek.csv

Python 3.7 vagy újabb ajánlott.

## Telepítés

    Könyvtárak telepítése requirements mappában található
    Minden szükséges modul telepíthető a következő paranccsal:
        pip install -r requirements.txt
    Vagy futtatsd az install_modules.py fájlt, amely automatikusan telepíti a függőségeket:
        python install_modules.py


## Használat

1.	Futtasd a fő programot:	python start_project.py

-   Adatbázis létrehozás/frissítés:
    Töltsd fel a CSV-ket, majd kattints az „Adatbázis frissítése” gombra. Ez beolvassa, tisztítja az adatokat, majd rögzíti őket az SQLite adatbázisba.

-   Táblák böngészése:
    Válassz ki egy táblát (adag vagy hutes) és nézd meg annak tartalmát.

-   Lekérdezések:
    A megfelelő gombra kattintva kész lekérdezéseket futtathatsz (panel-átlagok, legnagyobb értékek, időintervallum, stb.).

-   Új rekord beszúrása:
    (Ha beépíted: egy egyszerű űrlapon keresztül további adagszámot vagy hőfokadatot is adhatsz hozzá az adatbázishoz.)

## Fájlok magyarázata

-   project.py – A teljes alkalmazás logikája, Streamlit UI és adatfeldolgozás.
-   data/Adagok.csv – Forrásadat a gyártási adagokról.
-   data/Hűtőpanelek.csv – Forrásadat a szenzoros panelmérésekről.
-   data/Kemence.db – Az automatikusan generált SQLite adatbázisfájl.

## Fő funkciók

-   CSV adatok intelligens tisztítása, normalizálása (hibás, irreális, hiányzó értékek kezelése)
-   Adatbázis generálás, frissítés, tranzakciókezeléssel
-   Táblák böngészése modern Streamlit-felületen
-   Beépített SQL-lekérdezések: aggregáció, JOIN, UNION, időintervallumos lekérdezések stb.
-   új rekord beszúrása felületen keresztül
-   Felhasználói hibakezelés (siker, figyelmeztetés, hibaüzenetek)
	
## Működés
A program lehetővé teszi:
Adatbázis frissítését vagy újrahúzását, ha változott az adatforrás.
Felhasználók által táblanézetben történő adatellenőrzést.
Ipari- és adatbázis-mérnöki szempontból legfontosabb kérdések gyors áttekintését (statisztikák, szélsőértékek felderítése).
(Bővíthető) az adatok manuális bővítése vagy tesztelése érdekében.

## Közreműködők

-   [VérFürdő]