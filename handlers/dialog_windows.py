from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, User, ContentType
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Column, Start, Url, Group, Back, Cancel
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media import DynamicMedia


from bot_states.base_states import Menu, PrizeDraw
from .dialogs_getters.getters import username_getter
from .dialog_handlers.callback_logic import ask_question_button, products_60_120, products_75_150


router_dialog = Router()

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
        getter=username_getter,
        state=Menu.start
    ),
    Window(
        Const('Вы можете задать свой вопрос в нашем чате.\nhttps://t.me/RichCat_help_bot'),
        Column(
            Back(
                Const('◀️'),
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
                Const('◀️'),
                id='back',
                state=Menu.start
            )
        ),
        state=Menu.product_size
    ),
    Window(
        Const('Ссылки на товар'),
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
                Const('◀️'),
                id='back',
                state=Menu.start
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
            Url(
                text=Const('194079891'),
                url=Const(
                    'https://www.wildberries.ru/catalog/194079891/detail.aspx'),
                id='194079891'),
        ),
        Row(
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
                state=Menu.start
            )
        ),
        state=Menu.Url_75_150
    )
)


prize_dilog = Dialog(
    Window
    (
        Const('''Благодарим за выбор нашего бренда. Это нас очень вдохновляет продолжать Вас радовать.
Для нас важно Ваше мнение о наших коврах.
Поэтому мы решили КАЖДЫЙ МЕСЯЦ проводить РОЗЫГРЫШ
среди любимых покупателей за отзыв и дарить один из
наших прекрасных КОВРИКОВ из эко-меха 60*120 см
(цвет выберет победитель из тех, что в наличии)

УСЛОВИЯ УЧАСТИЯ:
Вам нужно оставить отзыв в феврале 2024, марте 2024:
Напишите, что вам понравилось в коврах RichCat
Прикрепите фото (это по желанию, но нам будет приятно).
За каждый новый отзыв Вам присваивается порядковый номер для розыгрыша, который будет Вам прислан после выполнения условий

❗️Обратите внимание на то, чтобы наш секретный вкладыш не попал в кадр. О нем знаем только мы с Вами😉

🚩Итоги подведём 8 апреля в нашем Telegram-канале https://t.me/richcatkovry

Для того, чтобы принять участие, выбирайте соответствующий пункт
'''),
        Group(
            Row(
                Start(text=Const("Далее"),
                      id='first_screen',
                      state=PrizeDraw.review_screenshot),
                Button(text=Const('Как оставить отзыв'),
                       id='das'),
                Start(
                    text=Const('Задать вопрос'),
                    id='ask_question_gift',
                    state=PrizeDraw.help_rich_cat
                )
            ),
            Column(
                Cancel(
                    Const('◀️'),
                    id='cansel_prize_dilog',
                ),
            )
        ),
        state=PrizeDraw.prize_condition
    ),
    Window(
        Const('Вы можете задать свой вопрос в нашем чате.\nhttps://t.me/RichCat_help_bot'),
        Column(
            Back(
                Const('◀️'),
                id='back',
            ),
        ),
        state=PrizeDraw.help_rich_cat),

)


@ router_dialog.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=Menu.start, mode=StartMode.RESET_STACK)
