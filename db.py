import sqlite3

def init_db():
    conn = sqlite3.connect("candidates.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_candidate(name, phone):
    conn = sqlite3.connect("candidates.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO candidates (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()

def get_all_candidates():
    conn = sqlite3.connect("candidates.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM candidates")
    rows = cur.fetchall()
    conn.close()
    return rows