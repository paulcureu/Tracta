import sqlite3
import pandas as pd
import os

def cauta_jucator(conn):
    nume = input("🔎 Scrie numele jucătorului: ")
    query = f"""
    SELECT player, team, map, side, "Rating_2.1", score
    FROM player_stats
    LEFT JOIN match_scores ON player_stats.match_url = match_scores.match_url
    WHERE player LIKE '%{nume}%' COLLATE NOCASE
    """
    df = pd.read_sql(query, conn)

    if df.empty:
        print(f"\n❌ Niciun jucător găsit care conține: '{nume}'")
    else:
        df = df.fillna("N/A")
        print(f"\n✅ Rezultate pentru '{nume}':")
        print(df.head(15))

def cauta_echipa(conn):
    echipa = input("🔎 Scrie numele echipei: ")
    mod = input("🧩 Vrei doar hărți individuale (fără All maps)? (y/N): ").strip().lower()

    # Dacă alege 'y', eliminăm 'All maps'
    map_filter = "AND map != 'All maps'" if mod == 'y' else ""

    query = f"""
    SELECT player, team, map, side, "Rating_2.1", score
    FROM player_stats
    LEFT JOIN match_scores ON player_stats.match_url = match_scores.match_url
    WHERE team LIKE '%{echipa}%' COLLATE NOCASE
    {map_filter}
    ORDER BY map
    """
    df = pd.read_sql(query, conn)

    if df.empty:
        print(f"\n❌ Nicio echipă găsită care conține: '{echipa}'")
        sugestii = pd.read_sql(f"""
        SELECT DISTINCT team FROM player_stats
        WHERE team LIKE '%{echipa[:3]}%' COLLATE NOCASE
        LIMIT 5
        """, conn)
        if not sugestii.empty:
            print("💡 Poate ai vrut una dintre:")
            print(sugestii)
    else:
        df = df.fillna("N/A")
        mod_descriere = "doar hărți individuale" if mod == 'y' else "toate hărțile (inclusiv All maps)"
        print(f"\n✅ Rezultate pentru echipa '{echipa}' ({mod_descriere}):")
        print(df.to_string(index=False))



def afiseaza_scoruri(conn):
    query = """
    SELECT DISTINCT score, match_url
    FROM match_scores
    ORDER BY match_url DESC
    LIMIT 15
    """
    df = pd.read_sql(query, conn)
    print("\n📋 Ultimele scoruri înregistrate:")
    print(df)

def afiseaza_meciuri_echipa(conn):
    echipa = input("🏆 Scrie numele echipei pentru a vedea meciurile: ")
    query = f"""
    SELECT DISTINCT ps.match_url, ms.score
    FROM player_stats ps
    LEFT JOIN match_scores ms ON ps.match_url = ms.match_url
    WHERE ps.team LIKE '%{echipa}%' COLLATE NOCASE
    """
    df = pd.read_sql(query, conn)

    if df.empty:
        print(f"\n❌ Niciun meci găsit pentru echipa '{echipa}'")
    else:
        df = df.fillna("N/A")
        print(f"\n✅ Meciuri găsite pentru echipa '{echipa}':")
        print(df)

def meniu():
    conn = sqlite3.connect("cs-db.db")
    while True:
        print("\n=== 🧠 Meniu Tracta ===")
        print("1. 🔎 Caută un jucător")
        print("2. 🛡️ Caută o echipă")
        print("3. 📊 Afișează scoruri + linkuri meci")
        print("4. 🏆 Afișează meciurile unei echipe")
        print("0. ❌ Ieșire")
        opt = input("Alege opțiunea: ")

        if opt == "1":
            cauta_jucator(conn)
        elif opt == "2":
            cauta_echipa(conn)
        elif opt == "3":
            afiseaza_scoruri(conn)
        elif opt == "4":
            afiseaza_meciuri_echipa(conn)
        elif opt == "0":
            print("👋 La revedere!")
            break
        else:
            print("⛔ Opțiune invalidă. Încearcă din nou.")
    conn.close()

if __name__ == "__main__":
    meniu()