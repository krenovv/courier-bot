from app.models.car_settings import CarSettings


class CarSettingsRepository:
    def __init__(self):
        self.settings = CarSettings(
            fuel_price=64.30,
            fuel_consumption_per_100km=12.3,
            amortization_per_km=2.14
        )

    def get(self):
        return self.settings