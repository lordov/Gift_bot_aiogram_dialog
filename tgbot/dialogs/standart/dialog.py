from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Column, Start, Url, Group, Back, Cancel
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media import StaticMedia


from tgbot.dialogs.states import Menu, GiveawayDialog, AdminPanel, PrizeDraw
from tgbot.dialogs.getters import username_getter, object_bot
from tgbot.dialogs.standart.callback import (
    process_review_screenshot, process_verification_screenshot
)


start_dialog = Dialog(
    Window(
        Format('start_greeting'),
        Row(
            Start(
                text=Const('Розыгрыш!'),
                id='prize_draw',
                state=GiveawayDialog.Start
            ),
        ),
        Column(
            Start(
                text=Const('Задать вопрос'),
                id='ask_question_gift',
                state=Menu.help
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
        state=Menu.help),
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
