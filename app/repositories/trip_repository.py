class TripRepository:

    def __init__(self):
        self.trips = []

    def save(self, trip):
        self.trips.append(trip)

    def get_all(self):
        return self.trips