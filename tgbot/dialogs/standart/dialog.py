from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Column, Start, Url, Group, Back, Cancel
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media import StaticMedia


from tgbot.dialogs.states import Menu, PrizeDraw, AdminPanel
from tgbot.dialogs.getters import username_getter, object_bot
from tgbot.dialogs.standart.callback import (
    products_60_120, products_75_150,
    process_review_screenshot, process_verification_screenshot)


start_dialog = Dialog(
    Window(
        Format('Привет, {username}!\n\
На связи команда RichCat. \n\
Спасибо, что выбрали нас! \n\n\
Здесь вы можете ознакомиться с нашим ассортиментом, а также принять участие в РОЗЫГРЫШЕ ЗА ОТЗЫВ\n\n\
Для этого выберите соответствующий пункт\n'),
        Row(
            Start(
                text=Const('Наши товары'),
                id='product',
                state=Menu.product_size
            ),
            Start(
                text=Const('Розыгрыш'),
                id='gift',
                state=PrizeDraw.prize_condition
            )
        ),
        Column(
            Start(
                text=Const('Задать вопрос'),
                id='ask_question_gift',
                state=Menu.help_rich_cat
            )
        ),
        Column(
            Start(
                text=Const('Админ панель'),
                id='start_admin_pnl',
                when='is_admin',
                state=AdminPanel.Start
            )
        ),
        getter=username_getter,
        state=Menu.Start
    ),
    Window(
        Const('Вы можете задать свой вопрос в нашем чате.\nhttps://t.me/RichCat_help_bot'),
        Column(
            Back(
                Const('◀️ Назад'),
                id='back',
            ),
        ),
        state=Menu.help_rich_cat),
    Window(
        Const('Выбор размера'),
        Row(
            Button(
                Const('60*120'),
                id='go_to_60_120',
                on_click=products_60_120,
            ),
            Button(
                Const('75*150'),
                id='go_to_75_150',
                on_click=products_75_150,
            ),
        ),
        Column(
            SwitchTo(
                Const('◀️ Назад'),
                id='back',
                state=Menu.Start
            )
        ),
        state=Menu.product_size
    ),
    Window(
        Const('<b>Ссылки на товар</b>'),
        Row(
            Url(
                text=Const('126758787'),
                url=Const(
                    'https://www.wildberries.ru/catalog/126758787/detail.aspx'),
                id='126758787'),
            Url(
                text=Const('194079890'),
                url=Const(
                    'https://www.wildberries.ru/catalog/194079890/detail.aspx'),
                id='194079890'),
            Url(
                text=Const('194079888'),
                url=Const(
                    'https://www.wildberries.ru/catalog/194079888/detail.aspx'),
                id='194079888'),
        ),
        Row(
            Url(
                text=Const('194079894'),
                url=Const(
                    'https://www.wildberries.ru/catalog/194079894/detail.aspx'),
                id='194079894'),
            Url(
                text=Const('126025374'),
                url=Const(
                    'https://www.wildberries.ru/catalog/126025374/detail.aspx'),
                id='126025374'),
            Url(
                text=Const('126756271'),
                url=Const(
                    'https://www.wildberries.ru/catalog/126756271/detail.aspx'),
                id='126756271'),
        ),
        Column(
            SwitchTo(
                Const('◀️ Назад'),
                id='back',
                state=Menu.Start
            )
        ),
        state=Menu.Url_60_120
    ),
    Window(
        Const('Ссылки на товар'),
        Row(
            Url(
                text=Const('194079892'),
                url=Const(
                    'https://www.wildberries.ru/catalog/194079892/detail.aspx'),
                id='194079892'),
            Url(
                text=Const('194079893'),
                url=Const(
                    'https://www.wildberries.ru/catalog/194079893/detail.aspx'),
                id='194079893'),
        ),
        Row(
            Url(
                text=Const('194079891'),
                url=Const(
                    'https://www.wildberries.ru/catalog/194079891/detail.aspx'),
                id='194079891'),
            Url(
                text=Const('128615052'),
                url=Const(
                    'https://www.wildberries.ru/catalog/128615052/detail.aspx'),
                id='194079894'),
            Url(
                text=Const('128603867'),
                url=Const(
                    'https://www.wildberries.ru/catalog/128603867/detail.aspx'),
                id='128603867'),
        ),
        Column(
            SwitchTo(
                Const('◀️'),
                id='back',
                state=Menu.Start
            )
        ),
        state=Menu.Url_75_150
    )
)


prize_dialog = Dialog(
    Window
    (
        Const('''Благодарим за выбор нашего бренда. 
Это нас очень вдохновляет продолжать Вас радовать.
Для нас важно Ваше мнение о наших коврах.

Поэтому мы решили раз в 2 МЕСЯЦА мы будем проводить 
РОЗЫГРЫШ среди любимых покупателей за отзыв и дарить один из наших прекрасных 
КОВРИКОВ из эко-меха 60*120 см (цвет выберет победитель из тех, что в наличии)

УСЛОВИЯ УЧАСТИЯ:
1. Подписка на наш канал  https://t.me/richcatkovry
2. Вам нужно оставить положительный отзыв в апреле 2024 - мае 2024 на WB или OZON:
Напишите, что вам понравилось в коврах RichCat
Прикрепите фото (это по желанию, но нам будет приятно).
За каждый новый отзыв Вам присваивается порядковый номер для розыгрыша, который будет Вам прислан после выполнения условий
❗️Обратите внимание на то, чтобы наш секретный вкладыш не попал в кадр. О нем знаем только мы с Вами😉
🚩Итоги подведём 8 июня в нашем Telegram-канале https://t.me/richcatkovry
Для того, чтобы принять участие, выбирайте соответствующий пункт
'''),
        Group(
            Row(
                Start(text=Const("Далее"),
                      id='first_screen',
                      state=PrizeDraw.review_screenshot),
                Start(text=Const('Как оставить отзыв'),
                      id='help_for_review',
                      state=PrizeDraw.help_for_review),
            ),
            Column(
                Cancel(
                    Const('◀️ Назад'),
                    id='cancel_prize_dialog',
                ),
            )
        ),
        state=PrizeDraw.prize_condition
    ),
    Window(
        Const('''Для того, чтобы оставить отзыв, Следуйте по пунктам, и у Вас все получится 🤍:

1️⃣ Зайдите в Личный кабинет
2️⃣ Найдите раздел “Покупки”
3️⃣ Выберите товар Richcat, который Вы приобрели.
4️⃣ Кликните на “Отзыв”, далее – “Оставить отзыв”
5️⃣ Напишите, чем Вам понравился наш бренд
6️⃣ Кликните “Опубликовать отзыв”
7️⃣ Сделайте скриншот готового отзыва
8️⃣ Сделайте скриншот нашего товара из раздела "Покупки"

Сначала отправьте скриншот готового отзыва в этот чат

'''),
        Column(
            Back(
                Const('◀️ Назад'),
                id='back_to_PrizeDraw',
            ),
        ),
        state=PrizeDraw.help_for_review
    ),
    Window(
        Const(text='''Для того, чтобы вам присваивался порядковый Номер в Розыгрыше необходимо отправить в этот чат два скриншота из вашего кабинета.
Сначала отправьте скриншот готового отзыва, как на примере.
⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️'''),
        StaticMedia(
            url='https://lakarti.ru/image/catalog/photo_for_bot/IMG_8256.JPG',
            type=ContentType.PHOTO
        ),
        MessageInput(
            func=process_review_screenshot,
            content_types=ContentType.PHOTO,
        ),
        Column(
            Cancel(
                Const('◀️ Назад'),
                id='cancel_prize_dialog',
            ),
        ),
        state=PrizeDraw.review_screenshot
    ),
    Window(
        Const(text='''Отлично! Теперь отправьте скриншот нашего товара из раздела "Покупки", как на примере.
⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️'''),
        StaticMedia(
            url='https://lakarti.ru/image/catalog/photo_for_bot/IMG_8255.JPG',
            type=ContentType.PHOTO
        ),
        MessageInput(
            func=process_verification_screenshot,
            content_types=ContentType.PHOTO,
        ),
        Column(
            Cancel(
                Const('◀️ Назад'),
                id='cancel_prize_dialog',
            ),
        ),
        getter=object_bot,
        state=PrizeDraw.purchase_screenshot
    ),
    Window(
        Const(text='Скриншоты успешно отправлены на проверку. Ожидайте результатов.'),
        Column(
            Cancel(
                Const('◀️ Вернуться на главную'),
                id='cancel_after_screenshots',
            ),
        ),
        state=PrizeDraw.finish
    )
)
