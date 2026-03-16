from app.models.trip import Trip


def calculate_trip(trip: Trip) -> None:
    fuel_used = trip.distance_km * trip.fuel_consumption_per_100km / 100
    fuel_cost = round(fuel_used * trip.fuel_price_per_l)
    amortization_cost = round(trip.amortization_per_km * trip.distance_km)
    profit = trip.payment - trip.fuel_cost - trip.amortization_cost

    trip.fuel_cost = fuel_cost
    trip.amortization_cost = amortization_cost
    trip.profit = profit

