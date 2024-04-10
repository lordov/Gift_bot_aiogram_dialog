from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, ContentType
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Column, Start, Url
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media import StaticMedia

from bot_states.base_states import Menu
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
                state=Menu.gift_condition
            )
        ),
        Column(
            Button(
                text=Const('Задать вопрос'),
                id='ask_question_gift',
                on_click=ask_question_button)
        ),
        getter=username_getter,
        state=Menu.start
    ),
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
    )
)


@ router_dialog.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=Menu.start, mode=StartMode.RESET_STACK)
