from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Trip:

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

