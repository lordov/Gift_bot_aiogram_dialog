import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage

from redis.asyncio.client import Redis
from redis.exceptions import ConnectionError

from aiogram_dialog import setup_dialogs

# from handlers.standart_handlers import router
from tgbot.database.engine import create_db
from tgbot.dialogs.Standart_dialog import start_dialog, prize_dialog
from tgbot.dialogs.admin_dialog import admin_panel
from tgbot.handlers import router_list
from tgbot.database.engine import async_session_maker
from tgbot.middlewares.db_session import DataBaseSession

from tgbot.utils.logger_config import configure_logging
from tgbot.utils.commands import set_commands
from tgbot.config import BOT_TOKEN


async def setup_dispatcher():
    """
    Функция для настройки диспетчера (Dispatcher).

    Пытается установить соединение с Redis и создает хранилище данных
    (RedisStorage) или, если соединение с Redis не удалось, использует
    хранилище данных в памяти (MemoryStorage).

    Returns:
        Dispatcher: Объект диспетчера aiogram.
    """
    redis = Redis()
    try:
        await redis.ping()
        storage = RedisStorage(
            redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True))
    except ConnectionError:
        print("Redis is not available, using MemoryStorage instead.")
        storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    return dp


async def setup_bot(dp: Dispatcher):
    """
    Функция для настройки бота (Bot).
    Здесь же регистрируем роутеры и диалоги.

    Args:
        dp (Dispatcher): Объект диспетчера aiogram.

    Returns:
        Bot: Объект бота aiogram.
    """
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    await set_commands(bot)
    dp.include_routers(*router_list)
    dp.include_routers(admin_panel, start_dialog, prize_dialog)
    dp.update.outer_middleware(DataBaseSession(session_pool=async_session_maker))
    setup_dialogs(dp)
    return bot


async def main():

    dp = await setup_dispatcher()
    bot = await setup_bot(dp)

    await create_db()
    await set_commands(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Запуск бота
if __name__ == '__main__':
    configure_logging()
    asyncio.run(main())
    print('тестово для automation.yml')
