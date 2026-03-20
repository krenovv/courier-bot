from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Trip:

    user_id: int

    # фактические данные поездки
    distance_km: float
    payment: int

    # параметры машины в момент поездки
    fuel_price_per_l: float
    fuel_consumption_per_100km: float
    amortization_per_km: float

    # финансовый результат
    fuel_cost: int | None = None
    amortization_cost: int | None = None
    profit: int | None = None

    created_at: datetime = field(default_factory=datetime.now)

    @property
    def total_expenses(self):
        return self.fuel_cost + self.amortization_cost


    @property
    def profit_per_km(self):
        return round(self.profit / self.distance_km,1) if self.distance_km else 0
