# Цикл лабораторних робіт (2-6) , що  реалізують BlockProcessor з SQL-бекендом.
## Структура проєкту:
* **lab2** - логіка обробки СVS- файлу для побудови ланцюжка блоків (Chain). Описуються класи Block  та Votes, відбувається валідація надійшовших данних та запис підходящих блоків до Chain, відсортованих за view
* **lab3** - створення структури власної бази даних (db). Наповнення бази даних.
* **lab4** - перенесення класів з 2 лабораторної роботи. Читається база даних, а її оброблені дані записуються до словників задля зручної подальшох роботи з інформацією. Текстовий вивід отриманих даних з таблиці.
* **lab5** - створення updater, який приймає та записує в окрему тимчасову базу даних інформацію з  CVS або з термінату. Ця база даних передається до BlockProcessor, який тепер обробляє безпосередньо db,  а не CVS.
* **lab6** - інтегрування бібліотеки pydantic у код 4 лабораторної роботи для автоматичної перевірки та типізації вхідних данних. Також створено окремий файл,  в якому описані тести (за допомгою pytest) до нашого коду.

### Схема lab2 
```mermaid
graph LR
    A[(lab2.csv)] --> B[Цикл по рядках файлу]
    B --> C{Що надійшло}

    %% Гілка Блоків
    C -- "block" --> D{ID валідний?}
    D -- Так --> E{Блок новий або <br/>view більший?}
    E -- Так --> F[Оновити запис у <br/>best_blocks]
    
    %% Гілка Голосів
    C -- "vote" --> G{ID валідний?}
    G -- Так --> H[Додати у <br/>votes: set]

    %% Об'єднання та фільтрація
    F --> I{Фінальна фільтрація}
    H --> I
    I -- "Vote(ID) in votes" --> J[Список valid_blocks]

    %% Сортування
    J --> K[Цикл по блоках]
    K --> L{Пошук місця в chain <br/>через b.view}
    L --> M[Вставка: chain.insert]
    M --> N[Вивід готового ланцюжка]
```

### Схема lab3
```mermaid
graph LR
    A([Початок]) --> B[sqlite3.connect: voting_system.db]
    B --> C[CREATE TABLE IF NOT EXISTS:<br/>BLOCKS, SOURCES, PERSONS, VOTES]
    
    subgraph D [Заповнення даних]
        C --> K[INSERT OR IGNORE: BLOCKS]
        K --> G[INSERT OR IGNORE: SOURCES]
        G --> E[INSERT OR IGNORE: PERSONS]
        E --> H[INSERT OR IGNORE: VOTES]
    end
    
    H --> I[ Збереження у файл]
    I --> J[SELECT * FROM PERSONS]
    J --> P[Вивід результату ]
    P --> L([Кінець])
```
### Схема lab4
```mermaid
graph LR
    A([ Початок]) --> B[ Ініціалізація DataLoader]
    B --> C[ Виклик методу класу]
    
    subgraph D [ Процес маппінгу даних]
        C --> F[ SQL запит до БД]
        F --> G[ dict conversion]
        G --> H[ Створення об'єкта dataclass]
    end
    
    H --> I[ Повернення об'єкта в main]
    I --> J[ Вивід даних у консоль]
    J --> K([ Закриття з'єднання])
```
### Схема lab5
```mermaid
graph TD
    subgraph A [ updater.py]
        A1[A1: Отримання даних Консоль/CSV] --> A2[ Валідація ID]
        A2 --> A3[ Запис у BLOCKS/VOTES]
        A3 --> A4[ Додавання в event_stream]
    end

    A4 -.-> DB[(blockchain.db)]

    subgraph B [B: Consumer - BlockProcessor.py]
        DB --> B1[B SELECT event WHERE processed=0]
        B1 --> B2{ Тип події?}
        B2 -- block --> B3[ Вивід деталей блоку]
        B2 -- vote --> B4[ Вивід голосу]
        B3 --> B5[ UPDATE event_stream: processed=1]
        B4 --> B5
        B5 --> B6[B6: Вивід ]
        B6 --> B7[Очищення]
    end

    B6 -- loop --> B1
```

### Схема lab5
```mermaid
graph TD
    subgraph T [T: Етап тестування - pytest]
        T1[ DataLoader] --> T2[ Запуск тестів]
        T2 --> T3{T3: Валідація пройдена?}
        T3 -- No [ValidationError] --> T4[ Тест пройдено успішно]
        T3 -- Yes --> T5[ Тест пройдено успішно]
    end

    subgraph M [M: Основна програма - main.py]
        A([ Початок]) --> B[ Ініціалізація DataLoader]
        B --> C[ Виклик методу класу]
        C --> F[ SQL запит до БД]
        F --> G[ dict conversion]
        G --> H[ Створення об'єкта dataclass]
        H --> I[ Повернення об'єкта в main]
        I --> J[ Вивід даних у консоль]
        J --> K([ Закриття з'єднання])
        

    end

    T -.-> M
    K --> W([H: Кінець])

    %% Стилізація
    style T fill:#fce4ec,stroke:#880e4f,stroke-dasharray: 5 5
    style E fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style B fill:#e1f5fe,stroke:#01579b


    
