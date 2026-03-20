def validate_distance(value) -> float:
    try:
        distance = float(value)
    except (TypeError, ValueError):
        raise ValueError("Пробег должен быть числом")

    if distance <= 0:
        raise ValueError("Пробег должен быть больше нуля")

    if distance > 15000:
        raise ValueError("Пробег выглядит слишком большим для одной поездки")

    return distance


def validate_payment(value) -> int:
    try:
        payment = int(value)
    except (TypeError, ValueError):
        raise ValueError("Оплата должна быть целым числом")

    if payment < 0:
        raise ValueError("Оплата не может быть отрицательной")

    if payment > 1000000:
        raise ValueError("Оплата выглядит слишком большой для одной поездки.\n"
                         "Вы перевозите что-то запрещенное?")

    return payment


def validate_fuel_price(value) -> float:
    try:
        fuel_price = float(value)
    except (TypeError, ValueError):
        raise ValueError("Цена топлива должна быть числом")

    if fuel_price < 0:
        raise ValueError("Цена топлива не может быть отрицательной")

    if fuel_price > 500:
        raise ValueError("Цена топлива выглядит слишком большой.\n"
                         "Убедитесь, что Вы вводите цену топлива в рублях за 1 литр")

    return fuel_price


def validate_fuel_consumption(value) -> float:
    try:
        fuel_consumption = float(value)
    except (TypeError, ValueError):
        raise ValueError("Расход топлива должен быть числом")

    if fuel_consumption <= 0:
        raise ValueError("Расход топлива должен быть больше нуля")

    if fuel_consumption > 120:
        raise ValueError("Расход топлива выглядит слишком большим.\n"
                         "Убедитесь, что Вы вводите расход топлива в литрах на 100 км пути")

    return fuel_consumption


def validate_amortization(value) -> float:
    try:
        amortization = float(value)
    except (TypeError, ValueError):
        raise ValueError("Амортизация должна быть числом")

    if amortization < 0:
        raise ValueError("Амортизация не может быть отрицательной")

    if amortization > 100:
        raise ValueError("Амортизация выглядит слишком большой.\n"
                         "Убедитесь, что Вы вводите амортизацию в рублях на 1 км пути")

    return amortization