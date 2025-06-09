import logging
from tgbot.database.models import User, Participation, GiveawaySettings
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from tgbot.utils.numbers import generate_participation_number


db_logger = logging.getLogger('db_logger')


async def insert_user_data(session: AsyncSession, chat_id: str, username: str, first_name: str, last_name: str ):
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


async def update_participation_number(session: AsyncSession, chat_id: str, ):
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


async def get_participation_value(session: AsyncSession, chat_id: str):
    try:
        result = await session.execute(select(User.participate).where(User.chat_id == chat_id))
        participation_value = result.scalars().first()
        return participation_value if participation_value else 0
    except SQLAlchemyError as e:
        db_logger.error(f"Error getting participation value: {e}")
        return 0


async def check_admin(session: AsyncSession, chat_id: str):
    try:
        result = await session.execute(select(User.is_admin).where(User.chat_id == chat_id))
        is_admin = result.scalars().first()
        return bool(is_admin)
    except SQLAlchemyError as e:
        db_logger.error(f"Error checking admin status: {e}")
        return False


async def check_is_winner(session: AsyncSession, chat_id: str):
    try:
        result = await session.execute(select(User.chat_id).where(User.chat_id == chat_id, User.participate == 1))
        winner = result.scalars().first()
        return bool(winner)
    except SQLAlchemyError as e:
        db_logger.error(f"Error checking winner status: {e}")
        return False


async def get_all_users(session: AsyncSession):
    try:
        result = await session.execute(select(User.chat_id).where(User.is_admin == 0))
        users = result.fetchall()
        return users[0]
    except SQLAlchemyError as e:
        db_logger.error(f"Error getting all users: {e}")
        return []


async def check_monthly_participation(session: AsyncSession, chat_id: int):
    """Проверяет, участвовал ли пользователь в розыгрыше текущего месяца"""
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    try:
        # Сначала получаем ID пользователя
        user_result = await session.execute(select(User.id).where(User.chat_id == chat_id))
        user_id = user_result.scalar_one_or_none()
        
        if not user_id:
            return False
            
        # Проверяем участие в текущем месяце
        result = await session.execute(
            select(Participation)
            .where(
                Participation.user_id == user_id,
                Participation.month == current_month,
                Participation.year == current_year
            )
        )
        participation = result.scalar_one_or_none()
        return bool(participation)
    except SQLAlchemyError as e:
        db_logger.error(f"Error checking monthly participation: {e}")
        return False


async def add_participation(session: AsyncSession, chat_id: int, screenshot_verified: bool = False):
    """Добавляет запись об участии пользователя в розыгрыше текущего месяца"""
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    try:
        # Получаем ID пользователя
        user_result = await session.execute(select(User.id).where(User.chat_id == chat_id))
        user_id = user_result.scalar_one_or_none()
        
        if not user_id:
            return None
            
        # Генерируем уникальный номер участия
        participation_number = generate_participation_number()
        
        # Создаем запись об участии
        new_participation = Participation(
            user_id=user_id,
            participation_number=participation_number,
            month=current_month,
            year=current_year,
            screenshot_verified=screenshot_verified
        )
        
        session.add(new_participation)
        
        # Обновляем данные пользователя
        await session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                last_participation_date=datetime.now(),
                participate=User.participate + 1,
                number_of_part=participation_number
            )
        )
        
        await session.commit()
        return participation_number
    except SQLAlchemyError as e:
        db_logger.error(f"Error adding participation: {e}")
        await session.rollback()
        return None


async def get_current_giveaway_settings(session: AsyncSession):
    """Получает настройки текущего розыгрыша"""
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    try:
        result = await session.execute(
            select(GiveawaySettings)
            .where(
                GiveawaySettings.month == current_month,
                GiveawaySettings.year == current_year,
                GiveawaySettings.active == True
            )
        )
        settings = result.scalar_one_or_none()
        return settings
    except SQLAlchemyError as e:
        db_logger.error(f"Error getting giveaway settings: {e}")
        return None


async def update_subscription_status(session: AsyncSession, chat_id: int, is_subscribed: bool):
    """Обновляет статус подписки пользователя на канал"""
    try:
        await session.execute(
            update(User)
            .where(User.chat_id == chat_id)
            .values(is_subscribed=is_subscribed)
        )
        await session.commit()
        return True
    except SQLAlchemyError as e:
        db_logger.error(f"Error updating subscription status: {e}")
        await session.rollback()
        return False


async def get_all_participants_by_month(session: AsyncSession, month: int = None, year: int = None):
    """Получает всех участников розыгрыша за указанный месяц"""
    if month is None:
        month = datetime.now().month
    if year is None:
        year = datetime.now().year
        
    try:
        result = await session.execute(
            select(User, Participation)
            .join(Participation, User.id == Participation.user_id)
            .where(
                Participation.month == month,
                Participation.year == year
            )
        )
        participants = result.fetchall()
        return participants
    except SQLAlchemyError as e:
        db_logger.error(f"Error getting participants: {e}")
        return []
