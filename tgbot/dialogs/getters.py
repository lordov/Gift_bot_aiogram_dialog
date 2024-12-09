from aiogram.types import User
from aiogram_dialog import DialogManager
from tgbot.database.orm_query import check_admin


async def username_getter(event_from_user: User, **kwargs):
    session = kwargs.get('session')
    is_admin = await check_admin(session, event_from_user.id)
    return {'username': event_from_user.username,
            'is_admin': is_admin}


async def object_bot(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    dialog_manager.dialog_data.update(bot=event_from_user.bot)
    return {'bot': event_from_user.bot}
