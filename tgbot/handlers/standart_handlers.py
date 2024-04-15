from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.DB.db import insert_user_data
from tgbot.dialogs.states import Menu


start_router = Router()


@start_router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    chat_id = message.chat.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    await insert_user_data(chat_id, username, first_name, last_name)
    await dialog_manager.start(state=Menu.start, mode=StartMode.RESET_STACK)
