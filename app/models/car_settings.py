from dataclasses import dataclass


@dataclass(frozen=True)
class CarSettings:
    fuel_price_per_l: float
    fuel_consumption_per_100km: float
    amortization_per_km: float

    def __post_init__(self):
        if self.fuel_price_per_l <= 0:
            raise ValueError("Fuel price must be positive")

        if self.fuel_consumption_per_100km <= 0:
            raise ValueError("Fuel consumption must be positive")

        if self.amortization_per_km < 0:
            raise ValueError("Amortization cannot be negative")
