# TripTrack Bot

Telegram bot for drivers (couriers, taxi) to track trips, expenses, and calculate real profit.

Demo: https://t.me/Trip_Track_Bot

---

## Overview

TripTrack is designed to help drivers understand their real earnings by accounting not only for revenue, but also for expenses such as fuel and vehicle costs.

The bot provides a simple and fast way to log trips and get a clear picture of net profit.

---

## Features

- Trip tracking
- Fuel and expense accounting
- Profit calculation (not just revenue)
- Car configuration and cost parameters
- Daily activity overview (via bot interaction)

---

## Architecture

The project follows a layered architecture:

- **Handlers** — Telegram interaction logic  
- **Services** — business logic  
- **Repositories** — database operations  
- **Models** — data structures  

A Finite State Machine (FSM) is used for step-by-step user input.

---

## Tech Stack

- Python
- Telegram Bot API
- SQLite
- FSM (state management)

---

## Why this project

Most drivers focus only on revenue, ignoring expenses like fuel, maintenance, and depreciation.

TripTrack shifts the focus to **net profit**, giving a more accurate understanding of actual earnings.

---

## Run locally

```
git clone https://github.com/krenovv/triptrack-bot
cd triptrack-bot
pip install -r requirements.txt

# создать .env файл
BOT_TOKEN=your_token

python main.py
```
---

# TripTrack Bot (RU)

Telegram-бот для водителей (курьеры, такси) для учета поездок, расходов и расчета реальной прибыли.

Бот: https://t.me/Trip_Track_Bot

---

## Описание

TripTrack помогает водителям понимать реальный доход, учитывая не только выручку, но и расходы: топливо, амортизацию и другие затраты.

Бот позволяет быстро фиксировать поездки и получать прозрачную картину чистой прибыли.

---

## Возможности

- Учет поездок  
- Учет топлива и расходов  
- Расчет прибыли (а не только выручки)  
- Настройки автомобиля  
- Обзор активности через Telegram  

---

## Архитектура

Проект построен с разделением на слои:

- **Handlers** — логика Telegram  
- **Services** — бизнес-логика  
- **Repositories** — работа с базой данных  
- **Models** — структуры данных  

Для пошагового ввода используется FSM (Finite State Machine).

---

## Технологии

- Python  
- Telegram Bot API  
- SQLite  
- FSM  

---

## Зачем этот проект

Многие водители ориентируются только на выручку, не учитывая расходы: топливо, обслуживание и амортизацию.  

TripTrack делает акцент на **чистой прибыли**, давая более точное понимание заработка.

---

## Установка

```
git clone https://github.com/krenovv/triptrack-bot
cd triptrack-bot
pip install -r requirements.txt

# создать .env файл
BOT_TOKEN=your_token

python main.py
```
