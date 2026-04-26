import typer
import sqlite3
import os
import re
from typing import List, Optional

app = typer.Typer()
hex_pattern = re.compile(r'^0x[0-9a-fA-f]+$|^\d+$')

def init_db():
    conn = sqlite3.connect('blockchain.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_stream (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            id TEXT NOT NULL,
            processed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

def data_to_db(data_type: str, entity_id: str, view_val: int= 0):
    conn = sqlite3.connect('blockchain.db')
    cursor = conn.cursor()
    try:
        if data_type == 'block':
            cursor.execute("INSERT OR IGNORE INTO BLOCKS (id, view, desc) VALUES (?,?,?)",
                          (entity_id, view_val, f"Block {entity_id}") )
        elif data_type == 'vote':
            cursor.execute("INSERT INTO VOTES (block_id, voter_id) VALUES(?,?)",
                        (entity_id, 0))
        cursor.execute("INSERT INTO event_stream (type, id, processed) VALUES (?, ?, 0)", 
                       (data_type, entity_id))
        conn.commit()

    except:
        print("error")

    finally:
        conn.close()



def main():
    print("Hello from lab5!")


if __name__ == "__main__":
    main()
