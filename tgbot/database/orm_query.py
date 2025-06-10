import logging
from tgbot.database.models import User, Participation, GiveawaySettings
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from tgbot.utils.numbers import generate_participation_number
from tgbot.config import settings as config


db_logger = logging.getLogger('db_logger')


async def insert_user_data(session: AsyncSession, chat_id: str, username: str, first_name: str, last_name: str):
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
        # Получаем пользователя
        result = await session.execute(select(User).where(User.chat_id == chat_id))
        user = result.scalar_one_or_none()

        if not user:
            return False

        # Проверяем, есть ли запись об участии в текущем месяце
        # Здесь мы предполагаем, что поле last_participation_date содержит дату последнего участия
        if user.last_participation_date:
            return (user.last_participation_date.month == current_month and
                    user.last_participation_date.year == current_year)
        return False
    except SQLAlchemyError as e:
        db_logger.error(f"Error checking monthly participation: {e}")
        return False


async def add_participation(session: AsyncSession, chat_id: int):
    """Добавляет запись об участии пользователя в розыгрыше текущего месяца"""
    try:
        # Получаем пользователя
        result = await session.execute(select(User).where(User.chat_id == chat_id))
        user = result.scalar_one_or_none()

        if not user:
            return None

        # Генерируем уникальный номер участия
        participation_number = generate_participation_number()

        # Обновляем данные пользователя
        user.last_participation_date = datetime.now()
        user.participate = user.participate + 1
        user.number_of_part = participation_number

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
            select(User)
            .where(
                User.last_participation_date != None,
                User.last_participation_date.month == month,
                User.last_participation_date.year == year
            )
        )
        participants = result.scalars().all()
        return participants
    except SQLAlchemyError as e:
        db_logger.error(f"Error getting participants: {e}")
        return []


async def create_or_update_giveaway_settings(session: AsyncSession, text: str, image_path: str = None, channel_id: str = None):
    """Создает или обновляет настройки розыгрыша для текущего месяца"""
    current_month = datetime.now().month
    current_year = datetime.now().year

    try:
        # Проверяем, существуют ли настройки для текущего месяца
        result = await session.execute(
            select(GiveawaySettings)
            .where(
                GiveawaySettings.month == current_month,
                GiveawaySettings.year == current_year
            )
        )
        settings = result.scalar_one_or_none()

        if settings:
            # Обновляем существующие настройки
            if text:
                settings.text = text
            if image_path:
                settings.image_path = image_path
            if channel_id:
                settings.channel_id = channel_id
            settings.active = True
        else:
            # Создаем новые настройки
            if not channel_id:
                channel_id = config.bot.channel_id

            settings = GiveawaySettings(
                month=current_month,
                year=current_year,
                text=text,
                image_path=image_path,
                channel_id=channel_id,
                active=True
            )
            session.add(settings)

        await session.commit()
        return settings
    except SQLAlchemyError as e:
        db_logger.error(f"Error updating giveaway settings: {e}")
        await session.rollback()
        return None


async def set_giveaway_image(session: AsyncSession, image_path: str):
    """Устанавливает изображение для текущего розыгрыша"""
    current_month = datetime.now().month
    current_year = datetime.now().year

    try:
        result = await session.execute(
            select(GiveawaySettings)
            .where(
                GiveawaySettings.month == current_month,
                GiveawaySettings.year == current_year
            )
        )
        settings = result.scalar_one_or_none()

        if settings:
            settings.image_path = image_path
            await session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db_logger.error(f"Error setting giveaway image: {e}")
        await session.rollback()
        return False


async def get_all_giveaway_settings(session: AsyncSession):
    """Получает все настройки розыгрышей"""
    try:
        result = await session.execute(
            select(GiveawaySettings)
            .order_by(GiveawaySettings.year.desc(), GiveawaySettings.month.desc())
        )
        settings = result.scalars().all()
        return settings
    except SQLAlchemyError as e:
        db_logger.error(f"Error getting all giveaway settings: {e}")
        return []
