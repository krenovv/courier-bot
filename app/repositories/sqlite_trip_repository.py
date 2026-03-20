import sqlite3
from datetime import datetime
from app.models.trip import Trip


class SQLiteTripRepository:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def save(self, trip: Trip):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO trips (
            user_id, created_at,
            distance_km, payment,
            fuel_price, fuel_consumption, amortization,
            fuel_cost, amortization_cost, profit
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trip.user_id,
            trip.created_at.isoformat(),

            trip.distance_km,
            trip.payment,

            trip.fuel_price_per_l,
            trip.fuel_consumption_per_100km,
            trip.amortization_per_km,

            trip.fuel_cost,
            trip.amortization_cost,
            trip.profit
        ))

        conn.commit()
        conn.close()

    def get_all(self, user_id: int) -> list[Trip]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            created_at,
            distance_km, payment,
            fuel_price, fuel_consumption, amortization,
            fuel_cost, amortization_cost, profit
        FROM trips
        WHERE user_id = ?
        ORDER BY created_at ASC
        """, (user_id,))

        rows = cursor.fetchall()
        conn.close()

        trips = []

        for row in rows:
            trip = Trip(
                user_id=user_id,
                distance_km=row[1],
                payment=row[2],
                fuel_price_per_l=row[3],
                fuel_consumption_per_100km=row[4],
                amortization_per_km=row[5],
            )

            trip.created_at = datetime.fromisoformat(row[0])
            trip.fuel_cost = row[6]
            trip.amortization_cost = row[7]
            trip.profit = row[8]

            trips.append(trip)

        return trips


    def delete_all(self, user_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM trips WHERE user_id = ?",
            (user_id,)
        )

        conn.commit()
        conn.close()