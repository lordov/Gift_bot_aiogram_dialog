from aiogram import Router, Bot, F, html
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram_dialog import DialogManager, StartMode
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest


from tgbot.DB.db import insert_user_data, check_admin, update_participation_number
from tgbot.dialogs.states import Menu, AdminPanel
from tgbot.utils.logger_config import logging
from tgbot.config_data.config import load_config, Config
from tgbot.services.delay_service.publisher import delay_message_deletion
from fluentogram import TranslatorRunner
from nats.js.client import JetStreamContext


start_router = Router()
handlers_logger = logging.getLogger('code_logger')
config: Config = load_config()


# @start_router.message(CommandStart())
# async def command_start_process(message: Message, dialog_manager: DialogManager):
#     chat_id = message.chat.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name
#     last_name = message.from_user.last_name
#     await insert_user_data(chat_id, username, first_name, last_name)
#     await dialog_manager.start(state=Menu.Start, mode=StartMode.RESET_STACK)


# Этот хэндлер срабатывает на команду /start
@start_router.message(CommandStart())
async def process_start_command(message: Message, i18n: TranslatorRunner):
    username = html.quote(message.from_user.full_name)
    await message.answer(text=i18n.hello.user(username=username))

# Этот хэндлер срабатывает на нажатие инлайн-кнопки


@start_router.message(Command('del'))
async def send_and_del_message(
    message: Message,
    i18n: TranslatorRunner,
    js: JetStreamContext,
    delay_del_subject: str
) -> None:

    delay = 3
    msg: Message = await message.answer(text=i18n.will.delete(delay=delay))

    await delay_message_deletion(
        js=js,
        chat_id=msg.chat.id,
        message_id=msg.message_id,
        subject=delay_del_subject,
        delay=delay
    )


@start_router.message(Command('admin'))
async def start_admin_dialog(message: Message, dialog_manager: DialogManager):
    chat_id = message.from_user.id
    if await check_admin(chat_id):
        await message.answer('Ты одмен')
        await dialog_manager.start(state=AdminPanel.Start)


@start_router.callback_query(F.data == "verification_yes")
async def process_verification_response(callback: CallbackQuery, state: FSMContext, bot: Bot):
    caption = callback.message.caption
    chat_id = caption.split(',')[0].strip('()')
    message_id = callback.message.message_id
    number = await update_participation_number(chat_id)
    text = f'''Поздравляем, Вы среди участников нашего розыгрыша, который состоится \
    5 февраля в 15.00 в прямом эфире в нашем телеграм-канале https://t.me/richcatkovry.\

Ваш порядковый номер <b>{number}</b>. Удачи!'''
    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
        # Убираем инлайн-клавиатуру
        await bot.edit_message_reply_markup(chat_id=config.admin, message_id=message_id, reply_markup=None)
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
    await bot.edit_message_reply_markup(
        chat_id=config.admin.admin,
        message_id=message_id,
        reply_markup=None
    )
    await callback.message.answer("Данные отклонены.")
