import typer
import sqlite3
import os
import re
from typing import List, Optional

app = typer.Typer()

HEX_PATTERN = re.compile(r'^0x[0-9a-fA-F]+$|^\d+$')

def init_db():
    conn = sqlite3.connect('blockchain.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BLOCKS (
            id TEXT PRIMARY KEY,
            view INTEGER DEFAULT 0,
            desc TEXT DEFAULT 'No description'
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS VOTES (
            block_id TEXT,
            voter_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            source_id INTEGER
        )
    """)
    
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

def save_to_db(data_type: str, entity_id: str, view_val: int = 0):
    conn = sqlite3.connect('blockchain.db')
    cursor = conn.cursor()
    try:
        d_type = data_type.lower()
        if d_type == 'block':
            cursor.execute("INSERT OR IGNORE INTO BLOCKS (id, view, desc) VALUES (?, ?, ?)", 
                           (entity_id, view_val, f"Block {entity_id}"))
        elif d_type == 'vote':
            cursor.execute("INSERT INTO VOTES (block_id, voter_id) VALUES (?, ?)", 
                           (entity_id, 0))
        
        #  запис у чергу подій
        cursor.execute("INSERT INTO event_stream (type, id, processed) VALUES (?, ?, 0)", 
                       (d_type, entity_id))
        conn.commit()
    except :
        print(f"Помилка ")
    finally:
        conn.close()

@app.command()
def main(
    raw_data: List[str] = typer.Argument(None),
    input_file: Optional[str] = typer.Option(None, "--file", "-f")
):
    final_entries = []
    if input_file:
        if not os.path.exists(input_file):
            print(f"Файл {input_file} не знайдено"); raise typer.Exit()
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = [item.strip() for item in line.split(',')]
                if len(parts) >= 2 and parts[1].lower() not in ['id', 'block_id']:
                    #  view 
                    v_val = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0
                    final_entries.append((parts[0], parts[1], v_val))
    elif raw_data:
        for item in raw_data:
            if ',' in item:
                p = item.split(',')
                final_entries.append((p[0].strip(), p[1].strip(), 0))

    added = 0
    for d_type, d_id, v_val in final_entries:
        if HEX_PATTERN.match(str(d_id)):
            save_to_db(d_type, str(d_id), v_val)
            added += 1
    print(f" додано: {added}")

if __name__ == "__main__":
    init_db()
    app()