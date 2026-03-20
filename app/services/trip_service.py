from app.models.trip import Trip
from app.calculator.trip_calculator import calculate_trip
from app.repositories.interfaces import TripRepository, CarSettingsRepository
from app.utils.validators import validate_distance, validate_payment


class TripService:

    def __init__(
            self,
            trip_repository: TripRepository,
            car_settings_repository: CarSettingsRepository
    ):
        self.trip_repository = trip_repository
        self.car_settings_repository = car_settings_repository

    def create_trip(self, user_id: int, distance_km: float, payment: int) -> Trip:

        distance_km = validate_distance(distance_km)
        payment = validate_payment(payment)

        car_settings = self.car_settings_repository.get(user_id)

        if car_settings is None:
            raise ValueError(
                "Не найдены настройки автомобиля.\n"
                "Пожалуйста, задайте настройки и попробуйте еще раз."
            )

        trip = Trip(
            user_id=user_id,
            distance_km=distance_km,
            payment=payment,
            fuel_price_per_l=car_settings.fuel_price_per_l,
            fuel_consumption_per_100km=car_settings.fuel_consumption_per_100km,
            amortization_per_km=car_settings.amortization_per_km,
        )

        calculate_trip(trip)

        self.trip_repository.save(trip)

        return trip


    def get_all_trips(self, user_id: int) -> list[Trip]:
        return self.trip_repository.get_all(user_id)


    def delete_all_trips(self, user_id: int):
        self.trip_repository.delete_all(user_id)