from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from tgbot.dialogs.states import GiveawayDialog
from tgbot.dialogs.getters import get_giveaway_data
from tgbot.database.orm_query import (
    check_monthly_participation,
    add_participation,
    get_current_giveaway_settings,
    update_subscription_status
)
from tgbot.kbd.keyboards import gift_yes_or_no
from tgbot.utils.subscription import check_user_subscription
from tgbot.config import settings


async def start_giveaway(message: Message, dialog_manager: DialogManager):
    """Начало диалога розыгрыша"""
    await dialog_manager.start(GiveawayDialog.start)


async def on_subscription_check(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Проверка подписки пользователя на канал"""
    session = dialog_manager.middleware_data.get("session")
    chat_id = callback.from_user.id

    # Получаем настройки розыгрыша
    settings = await get_current_giveaway_settings(session)
    if not settings:
        await callback.answer("Розыгрыш в настоящее время не активен.")
        await dialog_manager.done()
        return

    # Проверяем подписку
    # is_subscribed = await check_user_subscription(callback.bot, chat_id, settings.channel_id)

    # Обновляем статус подписки в БД
    await update_subscription_status(session, chat_id, is_subscribed=True)

    await dialog_manager.switch_to(GiveawayDialog.screenshot_upload)


async def process_screenshot(message: Message, button: Button, dialog_manager: DialogManager):
    """Обработка загруженного скриншота"""
    if not message.photo:
        await message.answer("Пожалуйста, отправьте скриншот как изображение.")
        return

    # Сохраняем второй скриншот (покупку)
    screenshot = message.photo[-1].file_id
    chat_id = message.chat.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    #  Достаем объект бота, который мы достали getterom
    bot: Bot = message.bot

    # Отправляем скриншоты в личный чат для проверки
    await bot.send_photo(
        settings.bot.admin_id,
        screenshot,
        reply_markup=gift_yes_or_no(),
        caption=f'{chat_id, username, first_name, last_name}'
    )

    await dialog_manager.switch_to(state=GiveawayDialog.wait_for_desicion, show_mode=ShowMode.SEND)
