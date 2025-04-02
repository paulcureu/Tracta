import sqlite3
import pandas as pd

# Calea spre baza de date și fișierul CSV
db_path = "cs-db.db"
csv_path = "../data/match-score.csv"  # înlocuiește cu calea ta dacă e diferită

# Conectare la baza de date
conn = sqlite3.connect(db_path)

# === 1. Încărcare CSV ===
df_csv = pd.read_csv(csv_path)

# === 2. Redenumire coloane pentru consistență ===
df_csv = df_csv.rename(columns={
    "Match URL": "match_url",
    "Score": "score"
})

# === 3. Elimină scoruri lipsă sau invalide ===
df_csv = df_csv.dropna(subset=["match_url", "score"])

# === 4. Încărcare match_url existente din baza de date ===
df_existing = pd.read_sql("SELECT DISTINCT match_url FROM player_stats", conn)

# === 5. Filtrare doar scoruri care apar în player_stats ===
df_valid = df_csv[df_csv["match_url"].isin(df_existing["match_url"])].copy()

# === 6. Salvare scoruri în tabelul match_scores ===
df_valid[["match_url", "score"]].to_sql("match_scores", conn, if_exists="append", index=False)

# === 7. Verificare ===
print(f"✅ S-au adăugat {len(df_valid)} scoruri valide în tabelul match_scores.")
conn.close()