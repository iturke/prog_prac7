import sqlite3

# 1. Підключення до бази даних
con = sqlite3.connect("voting_system.db")
# Важливо: вмикаємо перевірку зв'язків
#con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()

# 2. Створення таблиць (схема з твоїх діаграм)
cur.execute("""
CREATE TABLE IF NOT EXISTS BLOCKS (
    id TEXT PRIMARY KEY,
    view INTEGER,
    desc TEXT,
    img BLOB
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS SOURCES (
    id INTEGER PRIMARY KEY,
    ip_addr TEXT,
    country_code TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS PERSONS (
    id INTEGER PRIMARY KEY,
    name TEXT,
    addr TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS VOTES (
    block_id TEXT,
    voter_id INTEGER,
    timestamp DATETIME,
    source_id INTEGER,
)
""")


cur.execute("""
INSERT OR IGNORE INTO BLOCKS (id, view, desc) 
VALUES ('0x5a2f', 120, 'First Block')
""")

cur.execute("""
INSERT OR IGNORE INTO SOURCES (id, ip_addr, country_code) 
VALUES (10, '192.168.0.1', 'UA')
""")

cur.execute("""
INSERT OR IGNORE INTO PERSONS (id, name, addr) 
VALUES (1, 'Студент Мех-Мату', 'Львів, Ukraine')
""")

cur.execute("""
INSERT OR IGNORE INTO VOTES (block_id, voter_id, timestamp, source_id) 
VALUES ('0x5a2f', 1, '2026-03-11 11:00:00', 10)
""")

con.commit()

print("Дані успішно оброблено.")
res = cur.execute("SELECT * FROM PERSONS")
print(res.fetchall())