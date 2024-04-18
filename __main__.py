import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram_dialog import setup_dialogs

from environs import Env

# from handlers.standart_handlers import router
from tgbot.dialogs.Standart_dialog import start_dialog, prize_dialog
from tgbot.dialogs.admin_dialog import admin_panel
from tgbot.handlers import router_list

from tgbot.DB.db import create_user_table

from tgbot.utils.logger_config import configure_logging
from tgbot.constants import BOT_TOKEN


async def main():
    botS = Bot(token=BOT_TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    await create_user_table()
    # Инициализация бота
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_routers(*router_list)
    dp.include_routers(admin_panel, start_dialog, prize_dialog)

    setup_dialogs(dp)

    await botS.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(botS)


# Запуск бота
if __name__ == '__main__':
    configure_logging()
    asyncio.run(main())
    print('тестово для automation.yml')
