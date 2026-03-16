from dataclasses import dataclass

@dataclass
class TripResult:
    fuel_used: float
    fuel_cost: int
    amortization: int
    profit: int