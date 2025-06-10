from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Column, Start
from aiogram_dialog.widgets.text import Format, Const

from tgbot.dialogs.states import Menu, GiveawayDialog, AdminPanel
from tgbot.dialogs.getters import username_getter

start_dialog = Dialog(
    Window(
        Format('{start_greeting}'),
        Row(
            Start(
                text=Format('{giveaway_start_btn}'),
                id='prize_draw',
                state=GiveawayDialog.start
            ),
        ),
        # Column(
        #     Start(
        #         text=Const('Задать вопрос'),
        #         id='ask_question_gift',
        #         state=Menu.help
        #     )
        # ),
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
    )
)
