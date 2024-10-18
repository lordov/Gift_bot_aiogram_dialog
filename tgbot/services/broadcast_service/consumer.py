import logging
import json

from aiolimiter import AsyncLimiter
from datetime import datetime, timedelta, timezone
from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext
from nats.js.api import ConsumerConfig

logger = logging.getLogger(__name__)


class BroadcastMessageConsumer:
    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            bot: Bot,
            subject: str,
            stream: str,
            durable_name: str,
            rate_limit: int = 29

    ) -> None:
        self.nc = nc
        self.js = js
        self.bot = bot
        self.subject = subject
        self.stream = stream
        self.durable_name = durable_name
        self.rate_limit = rate_limit
        self.limiter = AsyncLimiter(max_rate=rate_limit, time_period=1)

    async def start(self) -> None:
        self.stream_sub = await self.js.subscribe(
            subject=self.subject,
            stream=self.stream,
            cb=self.on_message,
            durable=self.durable_name,
            manual_ack=True,
            config=ConsumerConfig(
                max_deliver=5,
                ack_wait=30
            )
        )

    async def on_message(self, msg: Msg):
        async with self.limiter:
            try:
                chat_id = int(msg.headers.get('Tg-Broadcast-Chat-ID'))
                message_data = json.loads(msg.data.decode('utf-8'))
                await send_broadcast_message(self.bot, chat_id, message_data)
                await msg.ack()
            except Exception as e:
                logger.error(f"Error sending message to {chat_id}: {e}")
                await msg.nak(delay=5)


async def send_broadcast_message(bot: Bot, chat_id: int, message_data: dict):
    text = message_data.get('text')
    photo = message_data.get('photo')
    url = message_data.get('url')

    if url:
        button = InlineKeyboardButton(
            text="Перейти", callback_data="broadcast_click", url=url)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    else:
        keyboard = None

    if photo:
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=text, reply_markup=keyboard)
    else:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
