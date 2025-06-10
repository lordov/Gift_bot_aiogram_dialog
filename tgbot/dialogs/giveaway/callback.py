from datetime import datetime
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media import DynamicMedia

from tgbot.dialogs.states import GiveawayDialog
from tgbot.dialogs.getters import get_giveaway_data
from tgbot.database.orm_query import (
    check_monthly_participation,
    add_participation,
    get_current_giveaway_settings,
    update_subscription_status
)
from tgbot.utils.subscription import check_user_subscription


async def start_giveaway(message: Message, dialog_manager: DialogManager):
    """Начало диалога розыгрыша"""
    await dialog_manager.start(GiveawayDialog.Start)


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
    is_subscribed = await check_user_subscription(callback.bot, chat_id, settings.channel_id)

    # Обновляем статус подписки в БД
    await update_subscription_status(session, chat_id, is_subscribed)

    if is_subscribed:
        await dialog_manager.switch_to(GiveawayDialog.ScreenshotUpload)
    else:
        await callback.answer("Вы не подписаны на канал. Пожалуйста, подпишитесь и попробуйте снова.")


async def process_screenshot(message: Message, dialog_manager: DialogManager):
    """Обработка загруженного скриншота"""
    if not message.photo:
        await message.answer("Пожалуйста, отправьте скриншот как изображение.")
        return

    # Здесь можно добавить логику для проверки скриншота
    # Например, использовать OCR для проверки даты покупки и статуса доставки

    # Для простоты сейчас просто принимаем любой скриншот
    dialog_manager.dialog_data["screenshot_verified"] = True
    await dialog_manager.switch_to(GiveawayDialog.Participation)


async def on_participate(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Обработка нажатия на кнопку участия"""
    session = dialog_manager.middleware_data.get("session")
    chat_id = callback.from_user.id

    # Проверяем подписку еще раз
    settings = await get_current_giveaway_settings(session)
    is_subscribed = await check_user_subscription(callback.bot, chat_id, settings.channel_id)

    if not is_subscribed:
        await callback.answer("Не вижу вашей подписки. Попробуйте еще раз.")
        await dialog_manager.switch_to(GiveawayDialog.SubscriptionCheck)
        return

    # Добавляем участие
    screenshot_verified = dialog_manager.dialog_data.get(
        "screenshot_verified", False)
    participation_number = await add_participation(session, chat_id, screenshot_verified)

    if participation_number:
        dialog_manager.dialog_data["participation_number"] = participation_number
        await dialog_manager.switch_to(GiveawayDialog.Participation)
    else:
        await callback.answer("Произошла ошибка при регистрации участия. Попробуйте позже.")
        await dialog_manager.done()
