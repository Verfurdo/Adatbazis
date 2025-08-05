# start_project.py - Indítófájl

# Szükséges modulok importálása
import os         # Operációs rendszerrel kapcsolatos műveletekhez (fájlok elérési útjának kezelése)
import subprocess # Külső parancsok futtatása Pythonból (Streamlit alkalmazás indítása)
import sys        # Rendszerspecifikus információk és műveletek (Python futtatókörnyezet elérési útjának lekérése)

# A fájl dinamikus elérési útjának meghatározása
script_dir = os.path.dirname(os.path.abspath(__file__))  # Megadja az aktuális fájl könyvtárát
project_path = os.path.join(script_dir, 'project', 'project.py')  # Az elérési útvonalat a "script_dir" alapján határozza meg függetlenül attól honnan indítod a programot

# A Streamlit alkalmazás indítása
print("Elindítjuk a Streamlit alkalmazást...")
subprocess.run([sys.executable, "-m", "streamlit", "run", project_path])

