from app.models.trip import Trip
from app.calculator.trip_calculator import calculate_trip


class TripService:

    def __init__(self, trip_repository, car_settings_repository):
        self.trip_repository = trip_repository
        self.car_settings_repository = car_settings_repository

    def create_trip(self, distance_km: float, payment: int) -> Trip:

        car_settings = self.car_settings_repository.get()

        if car_settings is None:
            raise ValueError("Car settings are not configured")

        trip = Trip(
            distance_km=distance_km,
            payment=payment,
            fuel_price_per_l=car_settings.fuel_price_per_l,
            fuel_consumption_per_100km=car_settings.fuel_consumption_per_100km,
            amortization_per_km=car_settings.amortization_per_km,
        )

        calculate_trip(trip)

        self.trip_repository.save(trip)

        return trip

    def get_all_trips(self):
        return self.trip_repository.get_all()