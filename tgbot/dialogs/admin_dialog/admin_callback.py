from aiogram.types import Message
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager

from tgbot.dialogs.states import AdminPanel
from tgbot.DB.db import check_is_winner


async def winner_message(message: Message, button: Button, dialog_manager: DialogManager):
    winner_id = message.text
    winner = await check_is_winner(winner_id)
    if not winner:
        await message.answer(
            f'Пользователь с {winner_id} не ялвяется участником конкурса')
        await dialog_manager.switch_to(state=AdminPanel.Start)
        return
    #  Достаем объект бота, который мы достали getterom
    bot: Bot = dialog_manager.dialog_data.get('bot')

    try:
        await bot.send_message(winner_id, text='Добрый день! Поздравляем Вас с Победой в нашем розыгрыше!\n\
Cвяжитесь с нами и выберем коврик и адрес отправки.\n\
https://t.me/Lakarti_sales')
    except TelegramForbiddenError as err:
        await message.answer('Пользователь заблокировал бота')
        await dialog_manager.switch_to(state=AdminPanel.Start)

    await message.reply('Пользователь получил сообщение.')
    await dialog_manager.switch_to(state=AdminPanel.Start)
