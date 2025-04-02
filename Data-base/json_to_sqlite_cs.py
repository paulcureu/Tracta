import sqlite3
import json
import os

# === Config ===
json_path = "../data/data-base.json"   # <-- Schimbă dacă fișierul are alt nume
db_path = "cs-db.db"

# === Creează conexiunea la baza de date ===
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# === Creează tabelul dacă nu există deja ===
cursor.execute("""
CREATE TABLE IF NOT EXISTS player_stats (
    match_url TEXT,
    map TEXT,
    side TEXT,
    team TEXT,
    player TEXT,
    kd TEXT,
    plus_minus TEXT,
    adr REAL,
    kast TEXT,
    rating TEXT
)
""")

# === Încarcă fișierul JSON ===
with open(json_path, "r", encoding="utf-8") as f:
    all_data = json.load(f)

rows_inserted = 0

# === Parcurge toate meciurile ===
for match in all_data:
    for match_url, maps in match.items():
        for map_name, modes in maps.items():
            for side, tables in modes.items():
                for table_key, table in tables.items():
                    if not table or len(table) < 2:
                        continue  # Tabel gol sau fără date

                    team = table[0][0]  # prima coloană este numele echipei

                    for row in table[1:]:  # exclude header
                        if len(row) != 6:
                            continue  # protecție dacă sunt linii incomplete

                        player, kd, pm, adr, kast, rating = row
                        cursor.execute("""
                        INSERT INTO player_stats (
                            match_url, map, side, team, player, kd,
                            plus_minus, adr, kast, rating
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            match_url, map_name, side, team, player,
                            kd, pm, float(adr), kast, rating
                        ))
                        rows_inserted += 1

# === Salvează și închide conexiunea ===
conn.commit()
conn.close()

print(f"✅ Baza de date '{db_path}' creată cu succes.")
print(f"📊 Număr total de statistici inserate: {rows_inserted}")
