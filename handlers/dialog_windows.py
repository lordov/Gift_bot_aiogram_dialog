from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, ContentType
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Column
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media import StaticMedia

from bot_states.base_states import Menu
from dialogs_getters.getters import username_getter
from dialog_handlers.callback_logic import ask_question_button, products_60_120, products_75_150


router_dialog = Router()

start_dialog = Dialog(
    Window(
        Format('Привет, {username}!\n\
На связи команда RichCat. \n\
Спасибо, что выбрали нас! \n\n\
Здесь вы можете ознакомиться с нашим ассортиментом, а также принять участие в РОЗЫГРЫШЕ ЗА ОТЗЫВ\n\n\
Для этого выберите соответствующий пункт\n'),
        Row(
            SwitchTo(
                text=Const('Наши товары'),
                id='product',
                state=Menu.product
            ),
            SwitchTo(
                text=Const('Розыгрыш'),
                id='gift',
                state=Menu.gift_condition
            )
        ),
        Column(
            Button(
                text='Задать вопрос',
                id='ask_question_gift',
                on_click=ask_question_button)
        ),
        getter=username_getter,
        state=Menu.start
    ),
    Window(
        Const('Выбор размера'),
        Row(
            SwitchTo(
                text=Const('60*120'),
                state=Menu.product_60_120,
            ),
            SwitchTo(
                text=Const('60*120'),
                state=Menu.product_60_120,
            )
        ),
        state=Menu.product_size
    ),
    Window(
        StaticMedia(url='https://basket-09.wbbasket.ru/vol1267/part126758/126758787/images/big/1.webp',
                    type=ContentType.PHOTO),
        StaticMedia(url='https://basket-13.wbbasket.ru/vol1940/part194079/194079890/images/big/1.webp',
                    type=ContentType.PHOTO),
        StaticMedia(url='https://basket-13.wbbasket.ru/vol1940/part194079/194079888/images/big/1.webp',
                    type=ContentType.PHOTO),
        StaticMedia(url='https://basket-13.wbbasket.ru/vol1940/part194079/194079894/images/big/1.webp',
                    type=ContentType.PHOTO),
        StaticMedia(url='https://basket-09.wbbasket.ru/vol1260/part126025/126025374/images/big/1.webp',
                    type=ContentType.PHOTO),
        StaticMedia(url='https://basket-09.wbbasket.ru/vol1267/part126756/126756271/images/big/1.webp',
                    type=ContentType.PHOTO)
    )

)


@router_dialog.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=Menu.start, mode=StartMode.RESET_STACK)
