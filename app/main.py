from app.services.trip_service import TripService
from app.repositories.trip_repository import TripRepository
from app.repositories.car_settings_repository import CarSettingsRepository


trip_repo = TripRepository()
settings_repo = CarSettingsRepository()

trip_service = TripService(trip_repo, settings_repo)