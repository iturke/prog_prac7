import sqlite3
from dataclasses import dataclass

@dataclass
class Block:
    id: str
    view: int
    desc: str
    img: bytes

    @staticmethod
    def get_by_id(loader, block_id):
        cursor = loader.con.cursor()
        cursor.execute("SELECT * FROM BLOCKS WHERE id = ?", (block_id,))
        row = cursor.fetchone()
        return Block(**dict(row)) if row else None

@dataclass
class Person:
    id: int
    name: str
    addr: str

    @staticmethod
    def find_by_name(loader, name_part):
        cursor = loader.con.cursor()
        cursor.execute("SELECT * FROM PERSONS WHERE name LIKE ?", (f"%{name_part}%",))
        return [Person(**dict(row)) for row in cursor.fetchall()]

@dataclass
class Vote:
    block_id: str
    voter_id: int
    timestamp: str
    source_id: int

    @staticmethod
    def get_votes_for_block(loader, block_id):
        cursor = loader.con.cursor()
        cursor.execute("SELECT * FROM VOTES WHERE block_id = ?", (block_id,))
        return [Vote(**dict(row)) for row in cursor.fetchall()]

class DataLoader:
    def __init__(self, db_path):
        self.con = sqlite3.connect(db_path)
        self.con.row_factory = sqlite3.Row 

    def get_all(self, table_name, cls):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        return [cls(**dict(row)) for row in cursor.fetchall()]

    def close(self):
        self.con.close()

def main():
    loader = DataLoader("voting_system.db")
    
    try:
        my_block = Block.get_by_id(loader, "0x5a2f")
        if my_block:
            print(f"Знайдено блок: {my_block.desc}")

        candidates = Person.find_by_name(loader, "Ivan")
        print(candidates)

        votes_count = Vote.get_votes_for_block(loader, "0x5a2f")
        print(f" голоси за 0x5a2f: {len(votes_count)}")

    except Exception as e:
        print(f"Помилка: {e}")
    
    loader.close()

if __name__ == "__main__":
    main()