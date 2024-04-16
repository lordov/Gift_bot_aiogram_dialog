from aiogram.types import User
from aiogram_dialog import DialogManager
from tgbot.DB.db import check_admin


async def username_getter(event_from_user: User, **kwargs):
    is_admin = await check_admin(event_from_user.id)
    return {'username': event_from_user.username,
            'is_admin': is_admin}


async def object_bot(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    dialog_manager.dialog_data.update(bot=event_from_user.bot)
    return {'bot': event_from_user.bot}
