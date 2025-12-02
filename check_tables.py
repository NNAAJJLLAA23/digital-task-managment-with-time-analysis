import sqlite3

# Povezivanje na bazu
conn = sqlite3.connect("tasks.db")
cur = conn.cursor()

# Dohvati sve tabele u bazi
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()

conn.close()

print("Tabele u bazi:", tables)

# Provjera da li postoji tabela 'users'
if ("users",) in tables:
    print("Tabela 'users' postoji ✅")
else:
    print("Tabela 'users' ne postoji ❌")
