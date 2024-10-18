import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage

from redis.asyncio.client import Redis
from redis.exceptions import ConnectionError

from aiogram_dialog import setup_dialogs

# from handlers.standart_handlers import router
from tgbot.dialogs.Standart_dialog import start_dialog, prize_dialog
from tgbot.dialogs.admin_dialog import admin_panel
from tgbot.dialogs.broadcast_dialog import broadcast_dialog
from tgbot.handlers import router_list
from fluentogram import TranslatorHub

from tgbot.DB.db import create_user_table

from tgbot.middlewares.i18n import TranslatorRunnerMiddleware
from tgbot.services.streams.start_stream import delayed_stream
from tgbot.utils.i18n import create_translator_hub
from tgbot.utils.logger_config import configure_logging
from tgbot.utils.commands import set_commands
from tgbot.utils.nats_connect import connect_to_nats
from tgbot.utils.start_consumer import start_broadcast_consumer, start_delayed_consumer
from tgbot.config_data.config import Config, load_config


# Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)


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


async def setup_bot(dp: Dispatcher, token: str):
    """
    Функция для настройки бота (Bot).
    Здесь же регистрируем роутеры и диалоги.

    Args:
        dp (Dispatcher): Объект диспетчера aiogram.

    Returns:
        Bot: Объект бота aiogram.
    """
    bot = Bot(token=token, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    await set_commands(bot)
    dp.include_routers(*router_list)
    dp.include_routers(admin_panel, start_dialog,
                       prize_dialog, broadcast_dialog)
    dp.update.middleware(TranslatorRunnerMiddleware())
    setup_dialogs(dp)
    return bot


async def main():
    config: Config = load_config()
    dp = await setup_dispatcher()
    bot = await setup_bot(dp, config.tg_bot.token)
    await create_user_table()

    # Подключаемся к Nats и получаем ссылки на клиент и JetStream-контекст
    nc, js = await connect_to_nats(servers=config.nats.servers)
    # await delayed_stream(js)

    # Создаем объект типа TranslatorHub
    translator_hub: TranslatorHub = create_translator_hub()
    
    await set_commands(bot)

    try:
        await asyncio.gather(
            dp.start_polling(
                bot,
                js=js,
                delay_del_subject=config.delayed_consumer.subject,
                broadcast_subject=config.broadcast_consumer.subject,
                _translator_hub=translator_hub
            ),
            start_delayed_consumer(
                nc=nc,
                js=js,
                bot=bot,
                subject=config.delayed_consumer.subject,
                stream=config.delayed_consumer.stream,
                durable_name=config.delayed_consumer.durable_name
            ),
            start_broadcast_consumer(
                nc=nc,
                js=js,
                bot=bot,
                subject=config.broadcast_consumer.subject,
                stream=config.broadcast_consumer.stream,
                durable_name=config.broadcast_consumer.durable_name,

            )
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await nc.close()
        logger.info('Connection to NATS closed')


# Запуск бота
if __name__ == '__main__':
    configure_logging()
    asyncio.run(main())
