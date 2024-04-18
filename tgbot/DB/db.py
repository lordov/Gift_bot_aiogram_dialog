import aiomysql
from tgbot.utils.numbers import generate_participation_number
from tgbot.utils.config import read_config
from tgbot.utils.logger_config import logging
from tgbot.constants import DB_HOST,  DB_DATABASE, DB_PASSWORD, DB_USER


db_logger = logging.getLogger('db_logger')


async def async_connect_to_db() -> aiomysql.Connection:
    try:
        connection = await aiomysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_DATABASE,
            auth_plugin="mysql_native_password",
        )
        return connection
    except aiomysql.Error as error:
        error_message = error.args[1]
        db_logger.error(f"Error connecting to the database: {error_message}")
        return None


async def create_user_table():
    async with await async_connect_to_db() as connection:
        try:
            async with connection.cursor() as cursor:
                # Создание базы данных richcat, если она не существует
                await cursor.execute("CREATE DATABASE IF NOT EXISTS richcat")
                # Использование базы данных richcat
                await cursor.execute("USE richcat")
                # Создание таблицы users
                await cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        chat_id VARCHAR(255) PRIMARY KEY,
                        username VARCHAR(255) NULL,
                        first_name VARCHAR(255) NULL,
                        last_name VARCHAR(255) NULL,
                        participate INT DEFAULT 0,
                        number_of_part VARCHAR(255) NULL,
                        is_admin TINYINT DEFAULT 0 NOT NULL
                    )
                """)
            await connection.commit()
        except aiomysql.Error as e:
            db_logger.error(f"Error creating user table: {e}")


async def insert_user_data(chat_id: str, username: str, first_name: str, last_name: str):
    async with await async_connect_to_db() as connection:
        try:
            async with connection.cursor() as cursor:
                await cursor.execute("""
                    SELECT * FROM users WHERE chat_id = %s
                """, (chat_id,))
                result = await cursor.fetchone()
                if not result:
                    await cursor.execute("""
                        INSERT INTO users (chat_id, username, first_name, last_name)
                        VALUES (%s, %s, %s, %s)
                    """, (chat_id, username, first_name, last_name))
                    await connection.commit()
        except aiomysql.Error as e:
            db_logger.error(f"Error inserting user data: {e}")


async def update_participation_number(chat_id: str):
    while True:
        participation_number = generate_participation_number()

        async with await async_connect_to_db() as connection:
            try:
                async with connection.cursor() as cursor:
                    await cursor.execute("""
                        SELECT chat_id
                        FROM users
                        WHERE number_of_part = %s
                    """, (participation_number,))
                    existing_chat_id = await cursor.fetchone()
            except aiomysql.Error as e:
                db_logger.error(
                    f"Error checking participation number uniqueness: {e}")

        if not existing_chat_id:
            break

        async with await async_connect_to_db() as connection:
            try:
                async with connection.cursor() as cursor:
                    await cursor.execute("""
                        UPDATE users
                        SET number_of_part = %s, participate = participate + 1
                        WHERE chat_id = %s
                    """, (participation_number, chat_id))
                    await connection.commit()
            except aiomysql.Error as e:
                db_logger.error(f"Error updating participation number: {e}")

    return participation_number


async def get_participation_value(chat_id: str):
    async with await async_connect_to_db() as connection:
        try:
            async with connection.cursor() as cursor:
                await cursor.execute("""
                    SELECT participate
                    FROM users
                    WHERE chat_id = %s
                """, (chat_id,))
                result = await cursor.fetchone()
        except aiomysql.Error as e:
            db_logger.error(f"Error getting participation value: {e}")

        return result[0] if result else 0


async def check_admin(chat_id: str):
    # Получение подключения к базе данных
    async with await async_connect_to_db() as connection:
        async with connection.cursor() as cur:
            cur: aiomysql.Cursor
            # Получение информации о пользователе из базы данных
            await cur.execute("SELECT is_admin FROM users WHERE chat_id = %s", (chat_id,))
            result = await cur.fetchone()

            return True if result[0] == 1 else False


async def check_is_winner(chat_id: str):
    async with await async_connect_to_db() as connection:
        try:
            async with connection.cursor() as cursor:
                cursor: aiomysql.Cursor
                await cursor.execute("""
                    SELECT chat_id FROM users WHERE `chat_id` = %s AND `participate` = '1'
                """, (chat_id,))
                result = await cursor.fetchone()
        except aiomysql.Error as e:
            db_logger.error(f"Error getting participation value: {e}")

        return True if result else False
