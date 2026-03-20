from app.services.trip_service import TripService
from app.services.car_settings_service import CarSettingsService
from app.repositories.sqlite_car_settings_repository import SQLiteCarSettingsRepository
from app.repositories.sqlite_trip_repository import SQLiteTripRepository
from types import SimpleNamespace


def build_container():
    db_path = "db.sqlite3"
    trip_repo = SQLiteTripRepository(db_path)
    car_repo = SQLiteCarSettingsRepository(db_path)

    trip_service = TripService(trip_repo, car_repo)
    car_settings_service = CarSettingsService(car_repo)

    return SimpleNamespace(
        trip_service=trip_service,
        car_settings_service=car_settings_service
    )