from aiogram.types import User
from aiogram_dialog import DialogManager
from tgbot.database.orm_query import (
    check_admin, check_monthly_participation,
    get_current_giveaway_settings)
from tgbot.dialogs.states import GiveawayDialog


async def username_getter(event_from_user: User, **kwargs):
    session = kwargs.get('session')
    is_admin = await check_admin(session, event_from_user.id)
    return {'username': event_from_user.username,
            'is_admin': is_admin}


async def object_bot(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    dialog_manager.dialog_data.update(bot=event_from_user.bot)
    return {'bot': event_from_user.bot}


async def get_giveaway_data(dialog_manager: DialogManager, **kwargs):
    """Получает данные для диалога розыгрыша"""
    session = dialog_manager.middleware_data.get("session")
    chat_id = dialog_manager.event.from_user.id

    # Проверяем участие в текущем месяце
    already_participated = await check_monthly_participation(session, chat_id)
    if already_participated:
        await dialog_manager.switch_to(GiveawayDialog.AlreadyParticipated)

    # Получаем настройки розыгрыша
    giveaway_settings = await get_current_giveaway_settings(session)

    # Получаем номер участия, если есть
    participation_number = dialog_manager.dialog_data.get(
        "participation_number", "")

    return {
        "already_participated": already_participated,
        "giveaway_settings": giveaway_settings,
        "participation_number": participation_number
    }
