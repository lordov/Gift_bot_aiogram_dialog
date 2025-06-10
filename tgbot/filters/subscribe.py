from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.client.bot import Bot


class IsSubscribe(BaseFilter):
    def __init__(self, channel_id: Union[int, str]):
        self.channel_id = channel_id

    async def __call__(self, message: Message, bot: Bot) -> bool:
        try:
            member = await bot.get_chat_member(
                chat_id=self.channel_id,
                user_id=message.from_user.id
            )
            if member.status not in ["member", "administrator", "creator"]:
                await message.answer("Вы не подписаны на канал. Пожалуйста, подпишитесь и попробуйте снова.")
                return False
            return True
        except Exception as e:
            await message.answer("Произошла ошибка при проверке подписки. Пожалуйста, попробуйте позже")
            return False
