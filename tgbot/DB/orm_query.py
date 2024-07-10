import logging
from DB.models import User
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.utils.numbers import generate_participation_number


db_logger = logging.getLogger('db_logger')


async def insert_user_data(chat_id: str, username: str, first_name: str, last_name: str, session: AsyncSession):
    try:
        result = await session.execute(select(User).where(User.chat_id == chat_id))
        user = result.scalars().first()
        if not user:
            new_user = User(chat_id=chat_id, username=username,
                            first_name=first_name, last_name=last_name)
            session.add(new_user)
            await session.commit()
    except SQLAlchemyError as e:
        db_logger.error(f"Error inserting user data: {e}")
        await session.rollback()


async def update_participation_number(chat_id: str, session: AsyncSession):
    while True:
        participation_number = generate_participation_number()

        try:
            result = await session.execute(select(User).where(User.number_of_part == participation_number))
            existing_user = result.scalars().first()
        except SQLAlchemyError as e:
            db_logger.error(
                f"Error checking participation number uniqueness: {e}")
            continue

        if not existing_user:
            break

    try:
        await session.execute(
            update(User)
            .where(User.chat_id == chat_id)
            .values(number_of_part=participation_number, participate=User.participate + 1)
        )
        await session.commit()
    except SQLAlchemyError as e:
        db_logger.error(f"Error updating participation number: {e}")
        await session.rollback()

    return participation_number


async def get_participation_value(chat_id: str, session: AsyncSession):
    try:
        result = await session.execute(select(User.participate).where(User.chat_id == chat_id))
        participation_value = result.scalars().first()
        return participation_value if participation_value else 0
    except SQLAlchemyError as e:
        db_logger.error(f"Error getting participation value: {e}")
        return 0


async def check_admin(chat_id: str, session: AsyncSession):
    try:
        result = await session.execute(select(User.is_admin).where(User.chat_id == chat_id))
        is_admin = result.scalars().first()
        return bool(is_admin)
    except SQLAlchemyError as e:
        db_logger.error(f"Error checking admin status: {e}")
        return False


async def check_is_winner(chat_id: str, session: AsyncSession):
    try:
        result = await session.execute(select(User.chat_id).where(User.chat_id == chat_id, User.participate == 1))
        winner = result.scalars().first()
        return bool(winner)
    except SQLAlchemyError as e:
        db_logger.error(f"Error checking winner status: {e}")
        return False
