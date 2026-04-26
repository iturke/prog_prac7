import sqlite3
import time

def process_new_events():
    # Підключаємося до бази
    conn = sqlite3.connect("blockchain.db")
    cursor = conn.cursor()

    print("BlockProcessor запущено. Очікування нових подій...")

    try:
        while True:
            # 1. Шукаємо в event_stream записи, які ще не були оброблені (processed = 0)
            cursor.execute("SELECT event_id, type, id FROM event_stream WHERE processed = 0")
            new_events = cursor.fetchall()

            if new_events:
                for event_id, e_type, e_id in new_events:
                    print(f"\n[ПОДІЯ] Виявлено нову активність: {e_type} (ID: {e_id})")

                    # 2. Логіка обробки залежно від типу
                    if e_type == 'block':
                        # Дістаємо дані про блок з основної таблиці
                        cursor.execute("SELECT id, view, desc FROM BLOCKS WHERE id = ?", (e_id,))
                        block_data = cursor.fetchone()
                        if block_data:
                            print(f" -> Обробка Блоку: {block_data[2]} (View: {block_data[1]})")
                    
                    elif e_type == 'vote':
                        # Дістаємо дані про голос
                        cursor.execute("SELECT block_id, voter_id FROM VOTES WHERE block_id = ?", (e_id,))
                        vote_data = cursor.fetchone()
                        if vote_data:
                            print(f" -> Зараховано голос за блок {e_id} від користувача {vote_data[1]}")

                    # 3. ПОЗНАЧАЄМО ЯК ПРОЧИТАНЕ (важливо за умовою!)
                    cursor.execute("UPDATE event_stream SET processed = 1 WHERE event_id = ?", (event_id,))
                
                # Зберігаємо зміни в БД
                conn.commit()
                print("-" * 30)
                print("Оновлення завершено. Чекаю наступних даних...")
            
            # Пауза 2 секунди, щоб не перевантажувати процесор
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nProcessor зупинено користувачем.")
    finally:
        conn.close()

if __name__ == "__main__":
    process_new_events()