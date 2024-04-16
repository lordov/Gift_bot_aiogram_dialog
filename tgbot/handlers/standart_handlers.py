from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.DB.db import insert_user_data, check_admin
from tgbot.dialogs.states import Menu, AdminPanel


start_router = Router()


@start_router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    chat_id = message.chat.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    await insert_user_data(chat_id, username, first_name, last_name)
    await dialog_manager.start(state=Menu.Start, mode=StartMode.RESET_STACK)


@start_router.message(Command('admin'))
async def start_admin_dialog(message: Message, dialog_manager: DialogManager):
    chat_id = message.from_user.id
    if await check_admin(chat_id):
        await message.answer('Ты одмен')
        await dialog_manager.start(state=AdminPanel.Start)
