import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram_dialog import setup_dialogs

# from handlers.standart_handlers import router
from handlers.dialog_windows import router_dialog, start_dialog, prize_dilog

from DB.db import create_user_table

from utils.config import read_config
from utils.logger_config import configure_logging


async def main():
    config = read_config('settings.ini')
    await create_user_table()
    # Инициализация бота
    botS = Bot(token=config["Tg"]["api_bot"], default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start_dialog)
    dp.include_router(prize_dilog)
    dp.include_router(router_dialog)

    setup_dialogs(dp)

    await botS.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(botS)


# Запуск бота
if __name__ == '__main__':
    configure_logging()
    asyncio.run(main())
