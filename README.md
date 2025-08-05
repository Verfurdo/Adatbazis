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

1.	Futtasd a fő programot:
	python start_project.py

## Használat

Indítás után egy konzolos menü jelenik meg, ahol a következő opciók közül választhatsz:
-	1 – Jegy Foglalása: Add meg a neved, a dátumot, majd válassz egy elérhető járatot.
-	2 – Foglalás Lemondása: Válaszd ki saját foglalásaid közül, melyiket szeretnéd törölni.
-	3 – Foglalások Listázása: Az összes foglalás megtekintése.
-	4 – Kilépés: A program bezárása.

## Fájlok magyarázata

-	GDE_Repjegy.py: A teljes program logikáját és konzolos kezelőfelületét tartalmazza.
	-	Jarat: Absztrakt alaposztály járatokhoz.
	-	Belfoldi / Europa / Amerika / Azsia: Származtatott osztályok - Konkrét járattípusok.
	-	JegyFoglalas: Foglalás adatait tárolja (járat, dátum, név).
	-	LegiTarsasag: Kezeli a járatokat és foglalásokat.
	
## Működés
A program elindulásakor a GDE-TOURS légitársaság előre feltöltött járatlistával és foglalásokkal rendelkezik. A felhasználó a menüben foglalhat jegyet, lekérdezheti vagy lemondhatja saját foglalásait.
A rendszer a dátum alapján ellenőrzi az elérhető járatokat. Minden foglalás egy JegyFoglalas objektumként kerül eltárolásra, ami tartalmazza a járat adatait, a foglalás dátumát és a felhasználó nevét.

## Közreműködők

-   [VérFürdő]