import sqlite3

conn = sqlite3.connect("cs-db.db")  # adaptează calea dacă e altundeva
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("📦 Tabele găsite în baza de date:")
for t in tables:
    print("-", t[0])

conn.close()
