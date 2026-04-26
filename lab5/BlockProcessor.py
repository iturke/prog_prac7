import sqlite3
import time

def start_processor():
    print("ЗАПУСТИЛОСЬ")
    
    while True:
        conn = sqlite3.connect('blockchain.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT event_id, type, id FROM event_stream WHERE processed = 0")
            events = cursor.fetchall()
            
            if events:
                for ev_id, e_type, e_id in events:
                    print(f"\n ID:{ev_id}  Тип:{e_type}")
                    
                    if e_type == 'block':
                        cursor.execute("SELECT view, desc FROM BLOCKS WHERE id = ?", (e_id,))
                        res = cursor.fetchone()
                        if res: 
                            print(f"  Блок: {res[1]}  VIEW: {res[0]}")
                    
                    elif e_type == 'vote':
                        print(f"  голос за: {e_id}")

                    cursor.execute("UPDATE event_stream SET processed=1 WHERE event_id = ?", (ev_id,))
                
                conn.commit()
                print(" очищено.")
            
        except :
            print(f"Помилка ")
        
        finally:
            conn.close()
            
        time.sleep(1) 

if __name__ == "__main__":
    start_processor()