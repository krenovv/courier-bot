# TripTrack Bot

Telegram-бот для учета поездок и расчета расходов (топливо, амортизация и т.д.)

## Возможности

- Добавление поездок
- Расчет стоимости поездки
- Хранение данных в SQLite
- Настройки автомобиля

## Архитектура

Проект построен с разделением на слои:

- Handlers (Telegram-логика)
- Services (бизнес-логика)
- Repositories (работа с БД)
- Models (структуры данных)

Используется FSM (Finite State Machine) для пошагового ввода данных.

## Установка

```
git clone https://github.com/krenovv/triptrack-bot
cd triptrack-bot
pip install -r requirements.txt
```

## Настройка

Создать .env файл:

```
BOT_TOKEN=your_token
```

## Запуск

```
python main.py
```
