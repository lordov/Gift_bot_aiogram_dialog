from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from aiogram import Bot
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager, ShowMode

from tgbot.dialogs.states import Menu, PrizeDraw
from tgbot.kbd.keyboards import gift_yes_or_no
from tgbot.DB.db import get_participation_value


async def ask_question_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    # Перенаправьте пользователя на чат для задания вопроса
    await callback.message.answer("Вы можете задать свой вопрос в нашем чате. https://t.me/RichCat_help_bot ")


async def products_60_120(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    photo_urls = [
        'https://basket-09.wbbasket.ru/vol1267/part126758/126758787/images/big/1.webp',
        'https://basket-13.wbbasket.ru/vol1940/part194079/194079890/images/big/1.webp',
        'https://basket-13.wbbasket.ru/vol1940/part194079/194079888/images/big/1.webp',
        'https://basket-13.wbbasket.ru/vol1940/part194079/194079894/images/big/1.webp',
        'https://basket-09.wbbasket.ru/vol1260/part126025/126025374/images/big/1.webp',
        'https://basket-09.wbbasket.ru/vol1267/part126756/126756271/images/big/1.webp',
    ]

    media_group = []
    for photo_url in photo_urls:
        media_group.append(InputMediaPhoto(media=photo_url))

    # Отправка фотографий в группе в одном сообщении
    await callback.message.answer_media_group(media=media_group)
    await dialog_manager.switch_to(state=Menu.Url_60_120, show_mode=ShowMode.SEND)

    # # Отправка ссылки на товар
    # await callback.message.answer(message_text, parse_mode='HTML')


async def products_75_150(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    photo_urls = [
        'https://basket-13.wbbasket.ru/vol1940/part194079/194079892/images/big/1.webp',
        'https://basket-13.wbbasket.ru/vol1940/part194079/194079893/images/big/1.webp',
        'https://basket-13.wbbasket.ru/vol1940/part194079/194079891/images/big/1.webp',
        'https://basket-09.wbbasket.ru/vol1286/part128615/128615052/images/big/1.webp',
        'https://basket-09.wbbasket.ru/vol1286/part128603/128603867/images/big/1.webp'
    ]

    media_group = []
    for photo_url in photo_urls:
        media_group.append(InputMediaPhoto(
            media=photo_url, show_mode=ShowMode.SEND))

    # Отправка фотографий в группе в одном сообщении
    await callback.message.answer_media_group(media=media_group)
    await dialog_manager.switch_to(state=Menu.Url_75_150, show_mode=ShowMode.SEND)


async def process_review_screenshot(message: Message, button: Button, dialog_manager: DialogManager):
    # Получение текущего значения participate
    chat_id = message.chat.id
    participate_value = await get_participation_value(chat_id)

    if participate_value == 1:
        # Добавить куда написать.
        text = "Вы уже участвуете в конкурсе! Если у вас появились вопросы напишите нам https://t.me/RichCat_help_bot ."
        await message.answer(text)
        # Возвращаем кентубрика обратно.
        await dialog_manager.switch_to(state=PrizeDraw.prize_condition, show_mode=ShowMode.SEND)

    # Сохраняем первый скриншот (отзыв)
    review_screenshot = message.photo[-1].file_id
    dialog_manager.dialog_data.update(review=review_screenshot)

    # Переходим к ожиданию первого скриншота (отзыва)
    await dialog_manager.switch_to(state=PrizeDraw.purchase_screenshot, show_mode=ShowMode.SEND)


async def process_verification_screenshot(message: Message, button: Button, dialog_manager: DialogManager):
    # Сохраняем второй скриншот (покупку)
    purchase_screenshot = message.photo[-1].file_id
    chat_id = message.chat.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    #  Достаем объект бота, который мы достали getterom
    bot: Bot = dialog_manager.dialog_data.get('bot')

    dialog_manager.dialog_data.update(purchase=purchase_screenshot)

    review_screenshot = dialog_manager.dialog_data.get('review')
    purchase_screenshot = dialog_manager.dialog_data.get('purchase')

    # Отправляем скриншоты в личный чат для проверки
    user_id_to_check = 502545728  # Замените на фактический идентификатор пользователя
    await bot.send_photo(user_id_to_check, review_screenshot)
    await bot.send_photo(user_id_to_check, purchase_screenshot, reply_markup=gift_yes_or_no(), caption=f'{chat_id, username, first_name, last_name}')

    await dialog_manager.switch_to(state=PrizeDraw.finish, show_mode=ShowMode.SEND)
