import sqlite3
from app.models.car_settings import CarSettings


class SQLiteCarSettingsRepository:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def get(self, user_id: int) -> CarSettings | None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT fuel_price, fuel_consumption, amortization FROM car_settings WHERE user_id = ?",
            (user_id,)
        )

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return CarSettings(
            user_id=user_id,
            fuel_price_per_l=row[0],
            fuel_consumption_per_100km=row[1],
            amortization_per_km=row[2],
        )

    def save(self, settings: CarSettings):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO car_settings (user_id, fuel_price, fuel_consumption, amortization)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            fuel_price = excluded.fuel_price,
            fuel_consumption = excluded.fuel_consumption,
            amortization = excluded.amortization
        """, (
            settings.user_id,
            settings.fuel_price_per_l,
            settings.fuel_consumption_per_100km,
            settings.amortization_per_km
        ))

        conn.commit()
        conn.close()


    def delete(self, user_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM car_settings WHERE user_id = ?",
            (user_id,)
        )

        conn.commit()
        conn.close()