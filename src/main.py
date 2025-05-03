import asyncio
from aiogram import Bot, Dispatcher
import logging
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from bot.utils.midlwares.album_middleware import AlbumMiddleware
from bot.config import bot_token
from bot.routers.admin.admin import router as admin_router
from bot.routers.admin.broadcast import router as broadcast_router
from bot.routers.balance.buy import router as buy_router
from bot.routers.menu.catalog import router as catalog_router
from bot.routers.main.kab import router as kab_router
from bot.routers.balance.pay import router as pay_router
from bot.routers.another.rerun import router as rerun_router
from bot.routers.main.start import router as start_router
from bot.routers.another.support import router as support_router

logging.basicConfig(level=logging.DEBUG)
async def main():
    bot = Bot(
        token=bot_token, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(AlbumMiddleware())
    dp.include_router(admin_router)
    dp.include_router(broadcast_router)
    dp.include_router(buy_router)
    dp.include_router(catalog_router)
    dp.include_router(kab_router)
    dp.include_router(pay_router)
    dp.include_router(rerun_router)
    dp.include_router(start_router)
    dp.include_router(support_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен!")