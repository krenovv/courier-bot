from app.models.car_settings import CarSettings
from app.repositories.interfaces import CarSettingsRepository
from app.utils.validators import validate_fuel_price, validate_fuel_consumption, validate_amortization


class CarSettingsService:

    def __init__(self, repository: CarSettingsRepository):
        self.repository = repository

    def get(self, user_id: int) -> CarSettings | None:
        return self.repository.get(user_id)

    def set(
            self,
            user_id: int,
            fuel_price_per_l: float,
            fuel_consumption_per_100km: float,
            amortization_per_km: float
    ) -> CarSettings:

        fuel_price_per_l = validate_fuel_price(fuel_price_per_l)
        fuel_consumption_per_100km = validate_fuel_consumption(fuel_consumption_per_100km)
        amortization_per_km = validate_amortization(amortization_per_km)

        car_settings = CarSettings(
            user_id=user_id,
            fuel_price_per_l=fuel_price_per_l,
            fuel_consumption_per_100km=fuel_consumption_per_100km,
            amortization_per_km=amortization_per_km
        )

        self.repository.save(car_settings)

        return car_settings


    def delete(self, user_id: int):
        self.repository.delete(user_id)