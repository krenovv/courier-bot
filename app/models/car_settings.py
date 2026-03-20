from dataclasses import dataclass


@dataclass(frozen=True)
class CarSettings:

    user_id: int
    fuel_price_per_l: float
    fuel_consumption_per_100km: float
    amortization_per_km: float