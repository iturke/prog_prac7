import sqlite3
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

class Block(BaseModel):
    id: str = Field(pattern=r"^0x[0-9a-fA-F]+")
    view: int = Field(ge=0) 
    desc: Optional[str] = None
    img: Optional[bytes] = None

    @staticmethod
    def get_by_id(loader, block_id: str) -> Optional["Block"]:
        cursor = loader.con.cursor()
        cursor.execute("SELECT * FROM BLOCKS WHERE id = ?", (block_id,))
        row = cursor.fetchone()
        if row:
            return Block.model_validate(dict(row))
        return None

class Person(BaseModel):
    id: int
    name: str = Field(min_length=2)
    addr: str

    @staticmethod
    def find_by_name(loader, name_part: str) -> List["Person"]:
        cursor = loader.con.cursor()
        cursor.execute("SELECT * FROM PERSONS WHERE name LIKE ?", (f"%{name_part}%",))
        return [Person.model_validate(dict(row)) for row in cursor.fetchall()]

class Vote(BaseModel):
    block_id: str = Field(pattern=r"^0x[0-9a-fA-F]+")
    voter_id: int
    timestamp: str
    source_id: int

    @staticmethod
    def get_votes_for_block(loader, block_id: str) -> List["Vote"]:
        cursor = loader.con.cursor()
        cursor.execute("SELECT * FROM VOTES WHERE block_id = ?", (block_id,))
        return [Vote.model_validate(dict(row)) for row in cursor.fetchall()]

class DataLoader:
    def __init__(self, db_path):
        self.con = sqlite3.connect(db_path)
        self.con.row_factory = sqlite3.Row 

    def close(self):
        self.con.close()

def main():
    loader = DataLoader("voting_system.db")
    
    try:
        my_block = Block.get_by_id(loader, "0x5a2f")
        if my_block:
            print(f"Знайдено блок: {my_block.desc}")
        else:
            print("Блок не знайдено")

        candidates = Person.find_by_name(loader, "Ivan")
        print(f"Знайдено кандидатів: {len(candidates)}")
        for p in candidates:
            print(f"  - {p.name} (ID: {p.id})")

        votes = Vote.get_votes_for_block(loader, "0x5a2f")
        print(f"Кількість голосів за 0x5a2f: {len(votes)}")

    except ValidationError as e:
        print(f"Помилка валідації даних з БД: \n{e}")
    except Exception as e:
        print(f"Помилка виконання: {e}")
    
    finally:
        loader.close()

if __name__ == "__main__":
    main()