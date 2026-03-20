from aiogram.fsm.state import StatesGroup, State

class AddTrip(StatesGroup):
    distance = State()
    payment = State()


class CarSettings(StatesGroup):
    fuel_price = State()
    consumption = State()
    amortization = State()

    edit_fuel_price = State()
    edit_consumption = State()
    edit_amortization = State()