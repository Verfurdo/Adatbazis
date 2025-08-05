import streamlit as st
import sqlite3
import pandas as pd
import os

# --- Dinamikus elérési utak beállítása ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_adag_PATH = os.path.join(BASE_DIR, 'data', 'Adagok.csv')
CSV_hutes_PATH = os.path.join(BASE_DIR, 'data', 'Hűtőpanelek.csv')
DB_PATH = os.path.join(BASE_DIR, 'data','Kemence.db')

def adatbazis_generalasa_feltoltes():
    # --- Adagok betöltése és tisztítása ---
    df_adagok = pd.read_csv(
        CSV_adag_PATH,        # Adagok.csv fájl beolvasása
        sep=";",              # mezőelválasztó
        decimal=",",          # tizedespont helyett vessző
        encoding="ISO-8859-1",    # karakterkódolás magyar ékezetekhez
        names=["adagszam", "kezdet_datum", "kezdet_ido", "veg_datum", "veg_ido", "koz_ido", "adagido"], #  mezők nevei
        header=0,   # a mezők nevei az első sorban vannak
    )
    # Üres sorok törlése
    df_adagok.dropna(how='all', inplace=True)  
    
    # Dátum és idő oszlopok egyesítése egy időponttá
    df_adagok["kezdet"] = pd.to_datetime(df_adagok["kezdet_datum"] + ' ' + df_adagok["kezdet_ido"])
    df_adagok["veg"] = pd.to_datetime(df_adagok["veg_datum"] + ' ' + df_adagok["veg_ido"])
    
    # Feleslegessé vált oszlopok eltávolítása
    df_adagok.drop(columns=['kezdet_datum', 'kezdet_ido', 'veg_datum', 'veg_ido', 'koz_ido', 'adagido'], inplace=True)
    

    # --- Hűtőpanelek betöltése és tisztítása ---
    df_hutes = pd.read_csv(
        CSV_hutes_PATH, # Hűtőpanelek.csv fájl beolvasása
        sep=';',        # mezőelválasztó
        decimal=',',    # tizedespont helyett vessző
        header=0,       # a mezők nevei az első sorban vannak
        parse_dates=list(range(0, 14, 2)),  # páratlan oszlopokat értékként dátummá konvertálja
        names=[         #  mezők nevei
            'panel1_ido', 'panel1',
            'panel2_ido', 'panel2',
            'panel3_ido', 'panel3',
            'panel4_ido', 'panel4',
            'panel5_ido', 'panel5',
            'panel6_ido', 'panel6',
            # 'panel7_ido', 'panel7',  #  nincs panel7
            'panel8_ido', 'panel8',
            'panel9_ido', 'panel9',
            'panel10_ido', 'panel10',
            'panel11_ido', 'panel11',
            'panel12_ido', 'panel12',
            'panel13_ido', 'panel13',
            'panel14_ido', 'panel14',
            'panel15_ido', 'panel15'
        ]
    )
    # Ellenőrzés azonosságok keresése
    ido_oszlopok = df_hutes.iloc[:, ::2]
    azonos = ido_oszlopok.eq(ido_oszlopok.iloc[:, 0], axis=0).all().all()
    if not azonos:
        st.warning("Nem minden panelhez tartozó időadat azonos!")
        
    # Első időoszlop megtartása azonosak törlése
    ido_oszlopok_torol = df_hutes.columns[2::2]
    df_hutes.drop(columns=ido_oszlopok_torol, inplace=True)
    
    # Hőmérséklet adatok kerekítése 2 tizedesig
    df_hutes.iloc[:, 1:] = df_hutes.iloc[:, 1:].round(2)
    
    # Idő oszlop átnevezése egységesen 'ido'-ra
    df_hutes.rename(columns={'panel1_ido': 'ido'}, inplace=True)

    # --- Hiányzó panel7 oszlop és az oszlopok sorrendbe állítása ---
    elvart_sorrend = [
        'ido',
        'panel1', 'panel2', 'panel3', 'panel4',
        'panel5', 'panel6', 'panel7', 'panel8', 'panel9', 'panel10',
        'panel11', 'panel12', 'panel13', 'panel14', 'panel15'
    ]
    for oszlop in elvart_sorrend:
        if oszlop not in df_hutes.columns:
            df_hutes[oszlop] = None  # None értékkel tölti fel a hiányzó oszlopokat
    df_hutes = df_hutes[elvart_sorrend]

    # --- Hibás értékeket None-ra cserélése, sorok törlése nélkül ---
    panel_oszlopok = [c for c in df_hutes.columns if c != 'ido']
    df_hutes[panel_oszlopok] = df_hutes[panel_oszlopok].where(
        (df_hutes[panel_oszlopok] >= 0) & (df_hutes[panel_oszlopok] < 100)
    )


    # --- Adatok SQLite adatbázisba töltése ---
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("BEGIN")
        df_adagok.to_sql(
            'adag', conn,
            if_exists='replace',
            index=False,
            dtype={'adagszam': 'INTEGER', 'kezdet': 'TEXT', 'veg': 'TEXT'}
        )
        df_hutes.to_sql(
            'hutes', conn,
            if_exists='replace',
            index=False,
            dtype={'ido': 'TEXT'}
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        st.error("Adatbázis feltöltési hiba, visszaállítás történt: " + str(e))
    finally:
        conn.close()



# --- Streamlit UI felület ---
st.set_page_config(layout="wide")  # Széles elrendezés, több hely a táblázatoknak
st.title("Kemence adatbázis: adatfeltöltés és lekérdezések")

# Adatbázis frissítése gomb
if st.button("Adatbázis frissítése"):
    adatbazis_generalasa_feltoltes()
    st.success("Adatok sikeresen újratöltve.")

if not os.path.exists(DB_PATH):
    st.warning("Adatbázis nem található, létrehozom és feltöltöm a csv fájlok adataival.")
    adatbazis_generalasa_feltoltes()
    st.success("Az adatbázis elkészült.")

# Adatbázis táblák böngészése
conn = sqlite3.connect(DB_PATH)
st.header("Táblák tartalma")
valasztott_tabla = st.radio("Válassz táblát:", options=['Adagszám', 'Hűtőpanelek'])
if valasztott_tabla == "Adagszám":
    tabla_nev = "adag"
else:
    tabla_nev = "hutes"
df_megjelenitendo = pd.read_sql_query(f"SELECT * FROM {tabla_nev}", conn)
st.dataframe(df_megjelenitendo, use_container_width=True)


# --- Lekérdezések ---
st.header("Lekérdezések")

# 1) AGGREGÁCIÓ: Átlaghőmérsékletek panelenként
if st.button("AGGREGÁCIÓ: Átlaghőmérsékletek panelenként"):
    res = pd.read_sql_query(
        """
        SELECT 
            (CAST(SUBSTR(name, 6, 2) AS INTEGER)) as panel,
            AVG(value) as atlag
        FROM (
            SELECT 'panel1' as name, panel1 as value FROM hutes
            UNION ALL SELECT 'panel2', panel2 FROM hutes
            UNION ALL SELECT 'panel3', panel3 FROM hutes
            UNION ALL SELECT 'panel4', panel4 FROM hutes
            UNION ALL SELECT 'panel5', panel5 FROM hutes
            UNION ALL SELECT 'panel6', panel6 FROM hutes
            UNION ALL SELECT 'panel7', panel7 FROM hutes
            UNION ALL SELECT 'panel8', panel8 FROM hutes
            UNION ALL SELECT 'panel9', panel9 FROM hutes
            UNION ALL SELECT 'panel10', panel10 FROM hutes
            UNION ALL SELECT 'panel11', panel11 FROM hutes
            UNION ALL SELECT 'panel12', panel12 FROM hutes
            UNION ALL SELECT 'panel13', panel13 FROM hutes
            UNION ALL SELECT 'panel14', panel14 FROM hutes
            UNION ALL SELECT 'panel15', panel15 FROM hutes
        ) 
        GROUP BY panel
        ORDER BY panel
        """,
        conn
    )
    st.dataframe(res)

# 2) AGGREGÁCIÓ: Panelenként a legmagasabb hőmérséklet lekérdezése
if st.button("AGGREGÁCIÓ: Legmagasabb hőmérséklet panelenként"):
    query = """
    SELECT panel, MAX(homerseklet) AS max_homerseklet FROM (
        SELECT 'panel1' AS panel, panel1 AS homerseklet FROM hutes
        UNION ALL SELECT 'panel2', panel2 FROM hutes
        UNION ALL SELECT 'panel3', panel3 FROM hutes
        UNION ALL SELECT 'panel4', panel4 FROM hutes
        UNION ALL SELECT 'panel5', panel5 FROM hutes
        UNION ALL SELECT 'panel6', panel6 FROM hutes
        UNION ALL SELECT 'panel7', panel7 FROM hutes
        UNION ALL SELECT 'panel8', panel8 FROM hutes
        UNION ALL SELECT 'panel9', panel9 FROM hutes
        UNION ALL SELECT 'panel10', panel10 FROM hutes
        UNION ALL SELECT 'panel11', panel11 FROM hutes
        UNION ALL SELECT 'panel12', panel12 FROM hutes
        UNION ALL SELECT 'panel13', panel13 FROM hutes
        UNION ALL SELECT 'panel14', panel14 FROM hutes
        UNION ALL SELECT 'panel15', panel15 FROM hutes
    ) GROUP BY panel
    ORDER BY panel;
    """
    res = pd.read_sql_query(query, conn)
    st.dataframe(res)

# 3) SELECT: Megadott időintervallum hőfokai lekérdezés (pl. '2024-07-18 14:00:00' és '2024-07-18 14:10:00' között)
if st.button("SELECT: Panelhőmérsékletek megadott időintervallumban (példa 10 percre)"):
    query = """
        SELECT ido, panel1, panel2, panel3, panel4, panel5, panel6, panel7, panel8, panel9, panel10, panel11, panel12, panel13, panel14, panel15
        FROM hutes
        WHERE ido BETWEEN '2024-07-18 14:00:00' AND '2024-07-18 14:10:00'
        ORDER BY ido
    """
    res = pd.read_sql_query(query, conn)
    st.dataframe(res)

# 4) JOIN: Minden adagszámhoz hozzáadjuk a kezdő időpontot és összekapcsoljuk a hutes-táblával
if st.button("JOIN: Minden adagszám kezdő időpontjához a hűtőpanel1 hőmérséklete"):
    # Legkorábbi panel1 hőfok minden adag 'kezdet' idejéhez
    query = """
        SELECT a.adagszam, a.kezdet, h.panel1
        FROM adag a
        JOIN hutes h ON h.ido = a.kezdet
        ORDER BY a.kezdet
        LIMIT 15
    """
    res = pd.read_sql_query(query, conn)
    st.write("Minden adag kezdő panel1 hőfoka:")
    st.dataframe(res)

# 5) UNION: Mindegyik panel, amely max vagy min hőfokot valaha elérte
if st.button("UNION: Panelek, melyek elérték a min vagy max hőmérsékletet"):
    query = '''
    SELECT DISTINCT panel FROM (
        SELECT 'panel1' AS panel FROM hutes WHERE panel1 = (SELECT MAX(panel1) FROM hutes)
        UNION
        SELECT 'panel1' FROM hutes WHERE panel1 = (SELECT MIN(panel1) FROM hutes)
        UNION
        SELECT 'panel2' AS panel FROM hutes WHERE panel2 = (SELECT MAX(panel2) FROM hutes)
        UNION
        SELECT 'panel2' FROM hutes WHERE panel2 = (SELECT MIN(panel2) FROM hutes)
        UNION
        SELECT 'panel3' AS panel FROM hutes WHERE panel3 = (SELECT MAX(panel3) FROM hutes)
        UNION
        SELECT 'panel3' FROM hutes WHERE panel3 = (SELECT MIN(panel3) FROM hutes)
        UNION
        SELECT 'panel4' AS panel FROM hutes WHERE panel4 = (SELECT MAX(panel4) FROM hutes)
        UNION
        SELECT 'panel4' FROM hutes WHERE panel4 = (SELECT MIN(panel4) FROM hutes)
        UNION
        SELECT 'panel5' AS panel FROM hutes WHERE panel5 = (SELECT MAX(panel5) FROM hutes)
        UNION
        SELECT 'panel5' FROM hutes WHERE panel5 = (SELECT MIN(panel5) FROM hutes)
        UNION
        SELECT 'panel6' AS panel FROM hutes WHERE panel6 = (SELECT MAX(panel6) FROM hutes)
        UNION
        SELECT 'panel6' FROM hutes WHERE panel6 = (SELECT MIN(panel6) FROM hutes)
        UNION
        SELECT 'panel7' AS panel FROM hutes WHERE panel7 = (SELECT MAX(panel7) FROM hutes)
        UNION
        SELECT 'panel7' FROM hutes WHERE panel7 = (SELECT MIN(panel7) FROM hutes)
        UNION
        SELECT 'panel8' AS panel FROM hutes WHERE panel8 = (SELECT MAX(panel8) FROM hutes)
        UNION
        SELECT 'panel8' FROM hutes WHERE panel8 = (SELECT MIN(panel8) FROM hutes)
        UNION
        SELECT 'panel9' AS panel FROM hutes WHERE panel9 = (SELECT MAX(panel9) FROM hutes)
        UNION
        SELECT 'panel9' FROM hutes WHERE panel9 = (SELECT MIN(panel9) FROM hutes)
        UNION
        SELECT 'panel10' AS panel FROM hutes WHERE panel10 = (SELECT MAX(panel10) FROM hutes)
        UNION
        SELECT 'panel10' FROM hutes WHERE panel10 = (SELECT MIN(panel10) FROM hutes)
        UNION
        SELECT 'panel11' AS panel FROM hutes WHERE panel11 = (SELECT MAX(panel11) FROM hutes)
        UNION
        SELECT 'panel11' FROM hutes WHERE panel11 = (SELECT MIN(panel11) FROM hutes)
        UNION
        SELECT 'panel12' AS panel FROM hutes WHERE panel12 = (SELECT MAX(panel12) FROM hutes)
        UNION
        SELECT 'panel12' FROM hutes WHERE panel12 = (SELECT MIN(panel12) FROM hutes)
        UNION
        SELECT 'panel13' AS panel FROM hutes WHERE panel13 = (SELECT MAX(panel13) FROM hutes)
        UNION
        SELECT 'panel13' FROM hutes WHERE panel13 = (SELECT MIN(panel13) FROM hutes)
        UNION
        SELECT 'panel14' AS panel FROM hutes WHERE panel14 = (SELECT MAX(panel14) FROM hutes)
        UNION
        SELECT 'panel14' FROM hutes WHERE panel14 = (SELECT MIN(panel14) FROM hutes)
        UNION
        SELECT 'panel15' AS panel FROM hutes WHERE panel15 = (SELECT MAX(panel15) FROM hutes)
        UNION
        SELECT 'panel15' FROM hutes WHERE panel15 = (SELECT MIN(panel15) FROM hutes)
    )
    ORDER BY panel
    '''
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    st.dataframe(df)

# 6) SELECT: Mindegyik panel, hőmérséklet MIN/MAX értéke
if st.button("SELECT: Panel hőmérséklet MIN/MAX összesítés"):
    query = """
SELECT panel, 'min' AS tipus, MIN(ertek) AS homerseklet
FROM (
    SELECT 'panel1' AS panel, panel1 AS ertek FROM hutes
    UNION ALL SELECT 'panel2', panel2 FROM hutes
    UNION ALL SELECT 'panel3', panel3 FROM hutes
    UNION ALL SELECT 'panel4', panel4 FROM hutes
    UNION ALL SELECT 'panel5', panel5 FROM hutes
    UNION ALL SELECT 'panel6', panel6 FROM hutes
    UNION ALL SELECT 'panel7', panel7 FROM hutes
    UNION ALL SELECT 'panel8', panel8 FROM hutes
    UNION ALL SELECT 'panel9', panel9 FROM hutes
    UNION ALL SELECT 'panel10', panel10 FROM hutes
    UNION ALL SELECT 'panel11', panel11 FROM hutes
    UNION ALL SELECT 'panel12', panel12 FROM hutes
    UNION ALL SELECT 'panel13', panel13 FROM hutes
    UNION ALL SELECT 'panel14', panel14 FROM hutes
    UNION ALL SELECT 'panel15', panel15 FROM hutes
)
GROUP BY panel
UNION
SELECT panel, 'max' AS tipus, MAX(ertek) AS homerseklet
FROM (
    SELECT 'panel1' AS panel, panel1 AS ertek FROM hutes
    UNION ALL SELECT 'panel2', panel2 FROM hutes
    UNION ALL SELECT 'panel3', panel3 FROM hutes
    UNION ALL SELECT 'panel4', panel4 FROM hutes
    UNION ALL SELECT 'panel5', panel5 FROM hutes
    UNION ALL SELECT 'panel6', panel6 FROM hutes
    UNION ALL SELECT 'panel7', panel7 FROM hutes
    UNION ALL SELECT 'panel8', panel8 FROM hutes
    UNION ALL SELECT 'panel9', panel9 FROM hutes
    UNION ALL SELECT 'panel10', panel10 FROM hutes
    UNION ALL SELECT 'panel11', panel11 FROM hutes
    UNION ALL SELECT 'panel12', panel12 FROM hutes
    UNION ALL SELECT 'panel13', panel13 FROM hutes
    UNION ALL SELECT 'panel14', panel14 FROM hutes
    UNION ALL SELECT 'panel15', panel15 FROM hutes
)
GROUP BY panel
ORDER BY panel, tipus;
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    st.dataframe(df)

st.info("""
Az egyes gombokra kattintva különféle lekérdezéseket, összegzéseket kaphatunk.  
""")
conn.close()


# 7) INSERT: új sor hozzáadása az adag táblához
st.header("INSERT: Új adagszám beszúrása az adatbázisba")

with st.form("insert_adag_form"):
    new_adagszam = st.number_input("Adagszám", min_value=1, step=1)
    new_kezdet = st.text_input("Kezdet időpont (YYYY-MM-DD HH:MM:SS)")
    new_veg = st.text_input("Vég időpont (YYYY-MM-DD HH:MM:SS)")
    submitted = st.form_submit_button("Beszúrás")

    if submitted:
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(
                "INSERT INTO adag (adagszam, kezdet, veg) VALUES (?, ?, ?)",
                (new_adagszam, new_kezdet, new_veg)
            )
            conn.commit()
            conn.close()
            st.success("Sikeres beszúrás az adag táblába!")
        except Exception as e:
            st.error(f"Hiba beszúráskor: {e}")