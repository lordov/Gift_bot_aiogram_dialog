from aiogram.types import User


async def username_getter(event_from_user: User, **kwargs):
    return {'username': event_from_user.username}
