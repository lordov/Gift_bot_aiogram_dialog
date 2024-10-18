from aiogram.types import ContentType
from aiogram_dialog import Dialog,  Window
from aiogram_dialog.widgets.kbd import (
    Row, SwitchTo, Start,
    Column,  Group, Cancel,
)
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const


from tgbot.dialogs.states import AdminPanel, BroadcastPanel
from tgbot.dialogs.getters import username_getter, object_bot
from tgbot.dialogs.admin_dialog.admin_callback import winner_message


admin_panel = Dialog(
    Window(
        Const(text='Выбери действие'),
        Group(
            Row(
                SwitchTo(
                    Const(text='Розыгрыш'),
                    id='start_draw',
                    state=AdminPanel.Prize
                )
            ),
        ),
        Start(
            text=Const('Создать рассылку'),
            id="broadcast",
            state=BroadcastPanel.Text
        ),
        Column(
            Cancel(
                Const('◀️ Назад'),
                id='cncl_adm_dialog',
            ),
        ),
        state=AdminPanel.Start
    ),
    Window(
        Const(
            text='Введите id пользователя, которому хотите отправить сообщение о выйгрыше'),
        MessageInput(
            func=winner_message,
            content_types=ContentType.TEXT
        ),
        getter=object_bot,
        state=AdminPanel.Prize
    ),
)
