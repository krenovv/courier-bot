from app.models.car_settings import CarSettings


class MemoryCarSettingsRepository:
    def __init__(self):
        self.storage = {}

    def get(self, user_id: int):
        return self.storage.get(user_id)

    def save(self, settings: CarSettings):
        self.storage[settings.user_id] = settings