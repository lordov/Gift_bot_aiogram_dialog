from aiogram import Bot
from aiogram.exceptions import TelegramAPIError


async def check_user_subscription(bot: Bot, user_id: int, channel_id: int) -> bool:
    """Проверяет, подписан ли пользователь на указанный канал"""
    try:
        # Проверяем статус пользователя в канале
        member = await bot.get_chat_member(channel_id, user_id)
        
        # Список статусов, которые означают активную подписку
        subscription_statuses = ['creator', 'administrator', 'member']
        
        return member.status in subscription_statuses
    except TelegramAPIError as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False 