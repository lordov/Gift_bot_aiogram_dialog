from aiogram.types import User
from aiogram_dialog import DialogManager


async def username_getter(event_from_user: User, **kwargs):
    return {'username': event_from_user.username}


async def object_bot(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    dialog_manager.dialog_data.update(bot=event_from_user.bot)
    return {'bot': event_from_user.bot}
