from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest


from tgbot.database.orm_query import insert_user_data, check_admin, update_participation_number, get_all_users
from tgbot.dialogs.states import Menu, AdminPanel
from tgbot.utils.logger_config import logging
from tgbot.config import settings


start_router = Router()
handlers_logger = logging.getLogger('code_logger')


@start_router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager, session: AsyncSession):
    chat_id = message.chat.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    users = await get_all_users(session)
    await insert_user_data(session, chat_id, username, first_name, last_name)
    await dialog_manager.start(state=Menu.Start, mode=StartMode.RESET_STACK)


@start_router.message(Command('admin'))
async def start_admin_dialog(message: Message, dialog_manager: DialogManager):
    chat_id = message.from_user.id
    if await check_admin(chat_id):
        await message.answer('Ты админ')
        await dialog_manager.start(state=AdminPanel.Start)


@start_router.callback_query(F.data == "verification_yes")
async def process_verification_response(callback: CallbackQuery, state: FSMContext, bot: Bot, session: AsyncSession):
    caption = callback.message.caption
    chat_id = caption.split(',')[0].strip('()')
    message_id = callback.message.message_id
    number = await update_participation_number(session, chat_id)
    text = f'''Text для розыгрыша'''
    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
        # Убираем инлайн-клавиатуру
        await bot.edit_message_reply_markup(chat_id=settings.bot.admin_id, message_id=message_id, reply_markup=None)
        await callback.message.answer("Данные подтверждены")
    except TelegramBadRequest as e:
        print(e)


@start_router.callback_query(F.data == "verification_no")
async def process_verification_response(callback: CallbackQuery, state: FSMContext, bot: Bot):
    caption = callback.message.caption
    chat_id = caption.split(',')[0].strip('()')
    message_id = callback.message.message_id
    text = f'''Извините, но похоже, вы отправили не те скриншоты. Пожалуйста, отправьте корректные скриншоты.
Вы можете задать свой вопрос в нашем чате.'''
    await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
    await bot.edit_message_reply_markup(chat_id=settings.bot.admin_id, message_id=message_id, reply_markup=None)
    await callback.message.answer("Данные отклонены.")
