from app.models.car_settings import CarSettings
from repositories.car_settings_repository import CarSettingsRepository


class CarSettingsService:

    def __init__(self, repository: CarSettingsRepository):
        self.repository = repository

    def get(self) -> CarSettings:
        return self.repository.get()

    def set(self,
            fuel_price: float,
            fuel_consumption_per_100km: float,
            amortization_per_km: float
    ) -> CarSettings:

        car_settings = CarSettings(
            fuel_price=fuel_price,
            fuel_consumption_per_100km=fuel_consumption_per_100km,
            amortization_per_km=amortization_per_km
        )

        self.repository.save(car_settings)

        return car_settings