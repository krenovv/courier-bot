import os
import asyncio

from dotenv import load_dotenv

from app.container import build_container
from app.bot.main import run_bot
from app.db.database import init_db


async def main():
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN not found")

    proxy = os.getenv("PROXY_URL")

    container = build_container()

    init_db("db.sqlite3")

    await run_bot(token, container, proxy)


if __name__ == "__main__":
    asyncio.run(main())