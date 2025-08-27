import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import settings
from .db import init_db
from .routers.home import router as home_router
from .routers.flow import router as flow_router
from .routers.admin import router as admin_router
from .routers.stats import router as stats_router

async def main():
    if not settings.BOT_TOKEN:
        raise RuntimeError("Укажите BOT_TOKEN в .env")

    await init_db()

    bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(home_router)
    dp.include_router(flow_router)
    dp.include_router(admin_router)
    dp.include_router(stats_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
