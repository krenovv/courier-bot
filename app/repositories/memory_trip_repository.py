from models.trip import Trip


class MemoryTripRepository:

    def __init__(self):
        self.trips = []

    def save(self, trip: Trip):
        self.trips.append(trip)

    def get_all(self, user_id: int):
        return self.trips