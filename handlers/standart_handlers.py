import kbd.keyboards as keyboards
import asyncio

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InputMediaPhoto
from aiogram import exceptions
from aiogram import Bot

from DB.db import insert_user_data, update_participation_number, get_participation_value

from utils.logger_config import logging


standart_router = Router()
handlers_logger = logging.getLogger('code_logger')


@standart_router.callback_query(F.data == "verification_yes")
async def process_verification_response(callback: types.CallbackQuery, bot: Bot):
    caption = callback.message.caption
    chat_id = caption.split(',')[0].strip('()')
    number = await update_participation_number(chat_id)
    text = f'''Поздравляем, Вы среди участников нашего розыгрыша, который состоится \
    5 февраля в 15.00 в прямом эфире в нашем телеграм-канале https://t.me/richcatkovry.\
    
Ваш порядковый номер <b>{number}</b>. Удачи!'''
    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
        await callback.message.answer("Данные подтверждены")
    except exceptions.TelegramBadRequest as e:
        print(e)


@standart_router.callback_query(F.data == "verification_no")
async def process_verification_response(callback: types.CallbackQuery, bot: Bot):
    caption = callback.message.caption
    chat_id = caption.split(',')[0].strip('()')
    text = f'''Извините, но похоже, вы отправили не те скриншоты. Пожалуйста, отправьте корректные скриншоты.
Вы можете задать свой вопрос в нашем чате.'''
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboards.gift_ready_or_not(), parse_mode='HTML')
    await callback.message.answer("Данные отклонены.")


# @standart_router.message()
# async def cmd_default(message: types.Message):
#     await message.answer('Для получения информации введите команду /start .')
