from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager

from tgbot.dialogs.states import AdminPanel
from tgbot.database.orm_query import (
    check_is_winner,
    get_all_participants_by_month,
    get_all_users,
    get_current_giveaway_settings,
    create_or_update_giveaway_settings,
    set_giveaway_image
)
from tgbot.utils.excel_export import export_participants_to_excel, export_users_to_excel


async def winner_message(message: Message, button: Button, dialog_manager: DialogManager):
    session = dialog_manager.middleware_data.get("session")
    winner_id = message.text
    winner = await check_is_winner(session, int(winner_id))
    if not winner:
        await message.answer(
            f'Пользователь с {winner_id} не ялвяется участником конкурса')
        await dialog_manager.switch_to(state=AdminPanel.Start)
        return
    #  Достаем объект бота, который мы достали getterom
    bot: Bot = dialog_manager.dialog_data.get('bot')
    i18n = dialog_manager.middleware_data.get("i18n")
    try:
        await bot.send_message(winner_id, text=i18n.get('winner-message'))
    except TelegramForbiddenError:
        await message.answer('Пользователь заблокировал бота')
        await dialog_manager.switch_to(state=AdminPanel.Start)

    await message.reply('Пользователь получил сообщение.')
    await dialog_manager.switch_to(state=AdminPanel.Start)


async def on_export_participants(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Экспорт участников в Excel"""
    session = dialog_manager.middleware_data.get("session")

    # Получаем всех участников текущего месяца
    participants = await get_all_participants_by_month(session)

    if not participants:
        await callback.answer("Нет участников для экспорта.")
        return

    # Экспортируем в Excel
    file_path, file_name = await export_participants_to_excel(participants)

    # Отправляем файл
    await callback.message.answer_document(
        FSInputFile(file_path, filename=file_name),
        caption="Список участников розыгрыша"
    )
    await dialog_manager.switch_to(AdminPanel.GiveawaySettings)

async def on_export_users(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Экспорт пользователей в Excel"""
    session = dialog_manager.middleware_data.get("session")
    users = await get_all_users(session)
    if not users:
        await callback.answer("Нет пользователей для экспорта.")
        return
    
    file_path, file_name = await export_users_to_excel(users)
    await callback.message.answer_document(
        FSInputFile(file_path, filename=file_name),
        caption="Список пользователей"
    )
    await dialog_manager.switch_to(AdminPanel.GiveawaySettings)


async def on_set_giveaway_text(message: Message, button: Button, dialog_manager: DialogManager):
    """Обработка ввода текста для розыгрыша"""
    session = dialog_manager.middleware_data.get("session")
    text = message.text

    # Сохраняем текст в диалоговых данных для последующего использования
    dialog_manager.dialog_data["giveaway_text"] = text

    # Создаем или обновляем настройки розыгрыша
    await create_or_update_giveaway_settings(session, text=text)

    await message.answer("Текст розыгрыша успешно обновлен.")
    await dialog_manager.switch_to(AdminPanel.GiveawaySettings)


async def on_set_giveaway_image(message: Message, button: Button, dialog_manager: DialogManager):
    """Обработка загрузки изображения для розыгрыша"""
    if not message.photo:
        await message.answer("Пожалуйста, отправьте изображение.")
        return

    session = dialog_manager.middleware_data.get("session")

    # Получаем информацию о фото
    photo = message.photo[-1]  # Берем самое большое изображение
    file_id = photo.file_id

    # Сохраняем file_id в настройках розыгрыша
    await create_or_update_giveaway_settings(session, image_path=file_id)

    await message.answer("Изображение для розыгрыша успешно обновлено.")
    await dialog_manager.switch_to(AdminPanel.GiveawaySettings)


async def on_set_channel_id(message: Message, button: Button, dialog_manager: DialogManager):
    """Обработка ввода ID канала для проверки подписки"""
    session = dialog_manager.middleware_data.get("session")
    channel_id = message.text.strip()

    # Проверяем формат ID канала
    if not channel_id.startswith("@") and not channel_id.startswith("-100"):
        await message.answer("Неверный формат ID канала. Используйте формат @channel_name или -100...")
        return

    # Обновляем ID канала в настройках
    await create_or_update_giveaway_settings(session, text=None, channel_id=channel_id)

    await message.answer(f"ID канала для проверки подписки обновлен: {channel_id}")
    await dialog_manager.switch_to(AdminPanel.GiveawaySettings)
