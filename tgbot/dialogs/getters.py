from aiogram.types import User
from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog import DialogManager
from tgbot.database.orm_query import (
    check_admin, check_monthly_participation,
    get_current_giveaway_settings
)
from fluentogram import TranslatorRunner
from tgbot.config import settings as config


async def username_getter(
        event_from_user: User,
        i18n: TranslatorRunner,
        **kwargs):
    session = kwargs.get('session')
    is_admin = await check_admin(session, event_from_user.id)
    return {
        'username': event_from_user.username,
        'is_admin': is_admin,
        'start_greeting': i18n.get('start-greeting', username=event_from_user.username),
        "giveaway_start_btn": i18n.get('giveaway-start-btn')
    }


async def object_bot(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    dialog_manager.dialog_data.update(bot=event_from_user.bot)
    return {'bot': event_from_user.bot}


async def get_giveaway_data(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs):
    """Получает данные для диалога розыгрыша"""
    session = dialog_manager.middleware_data.get("session")
    chat_id = dialog_manager.event.from_user.id

    # Проверяем участие в текущем месяце
    already_been = await check_monthly_participation(session, chat_id)

    return {
        "ready_to_giveaway": not already_been,
        "giveaway_thanks": i18n.get('giveaway-thanks'),
        "not_ready_to_giveaway": already_been,
        "giveaway_already_participated": i18n.get('giveaway-already-participated'),
        "giveaway_welcome": i18n.get('giveaway-welcome'),
        "giveaway_start": i18n.get('giveaway-start'),
        "btn_back": i18n.get('btn-back'),
        "giveaway_screenshot_request": i18n.get('giveaway-screenshot-request'),
        "giveaway_follow_up": i18n.get('giveaway-follow-up'),
        "giveaway_close": i18n.get('giveaway-close'),
    }


async def get_giveaway_settings(dialog_manager: DialogManager, **kwargs):
    """Получает настройки розыгрыша для административной панели"""
    session = dialog_manager.middleware_data.get("session")

    # Получаем текущие настройки розыгрыша
    settings = await get_current_giveaway_settings(session)

    if settings:
        current_text = settings.text
        current_channel_id = settings.channel_id
        current_image_path = settings.image_path
    else:
        current_text = "Текст не задан"
        current_channel_id = "@lakartiphoto"
        current_image_path = None

    if current_image_path:
        photo = MediaAttachment(
            type=ContentType.PHOTO,
            file_id=MediaId(current_image_path))
    else:
        photo = None

    return {
        "current_text": current_text,
        "current_channel_id": current_channel_id,
        "photo": photo
    }
