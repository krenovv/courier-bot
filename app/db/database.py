import sqlite3


def init_db(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Таблица настроек авто
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS car_settings (
        user_id INTEGER PRIMARY KEY,
        fuel_price REAL NOT NULL,
        fuel_consumption REAL NOT NULL,
        amortization REAL NOT NULL
    )
    """)

    # Таблица поездок
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        created_at TEXT NOT NULL,

        distance_km REAL NOT NULL,
        payment INTEGER NOT NULL,

        fuel_price REAL NOT NULL,
        fuel_consumption REAL NOT NULL,
        amortization REAL NOT NULL,

        fuel_cost REAL NOT NULL,
        amortization_cost REAL NOT NULL,
        profit REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()