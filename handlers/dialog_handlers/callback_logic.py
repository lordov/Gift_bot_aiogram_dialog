from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager
from bot_states.base_states import Menu


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
    product_url = ['https://www.wildberries.ru/catalog/126758787/detail.aspx',
                   'https://www.wildberries.ru/catalog/194079890/detail.aspx',
                   'https://www.wildberries.ru/catalog/194079888/detail.aspx',
                   'https://www.wildberries.ru/catalog/194079894/detail.aspx',
                   'https://www.wildberries.ru/catalog/126025374/detail.aspx',
                   'https://www.wildberries.ru/catalog/126756271/detail.aspx'
                   ]

    message_text = (
        f'1: <a href="{product_url[0]}">126758787</a>\n'
        f'2: <a href="{product_url[1]}">194079890</a>\n'
        f'3: <a href="{product_url[2]}">194079888</a>\n'
        f'4: <a href="{product_url[3]}">194079894</a>\n'
        f'5: <a href="{product_url[4]}">126025374</a>\n'
        f'6: <a href="{product_url[5]}">126756271</a>'

    )

    media_group = []
    for photo_url in photo_urls:
        media_group.append(InputMediaPhoto(media=photo_url, caption="text"))

    # Отправка фотографий в группе в одном сообщении
    lol = await callback.message.answer_media_group(media=media_group)
    if lol:
        await dialog_manager.switch_to(state=Menu.Url_60_120)
    # # Отправка ссылки на товар
    # await callback.message.answer(message_text, parse_mode='HTML')


async def products_75_150(callback: CallbackQuery):
    photo_urls = [
        'https://basket-13.wbbasket.ru/vol1940/part194079/194079892/images/big/1.webp',
        'https://basket-13.wbbasket.ru/vol1940/part194079/194079893/images/big/1.webp',
        'https://basket-13.wbbasket.ru/vol1940/part194079/194079891/images/big/1.webp',
        'https://basket-09.wbbasket.ru/vol1286/part128615/128615052/images/big/1.webp',
        'https://basket-09.wbbasket.ru/vol1286/part128603/128603867/images/big/1.webp'
    ]
    product_url = ['https://www.wildberries.ru/catalog/194079892/detail.aspx',
                   'https://www.wildberries.ru/catalog/194079893/detail.aspx',
                   'https://www.wildberries.ru/catalog/194079891/detail.aspx',
                   'https://www.wildberries.ru/catalog/128615052/detail.aspx',
                   'https://www.wildberries.ru/catalog/128603867/detail.aspx']

    message_text = (
        f'1: <a href="{product_url[0]}">194079892</a>\n'
        f'2: <a href="{product_url[1]}">194079893</a>\n'
        f'3: <a href="{product_url[2]}">194079891</a>\n'
        f'4: <a href="{product_url[3]}">128615052</a>\n'
        f'5: <a href="{product_url[4]}">128603867</a>'
    )

    media_group = []
    for photo_url in photo_urls:
        media_group.append(InputMediaPhoto(media=photo_url, caption="text"))

    # Отправка фотографий в группе в одном сообщении
    await callback.message.answer_media_group(media=media_group)

    # Отправка ссылки на товар
    await callback.message.answer(message_text, parse_mode='HTML')
