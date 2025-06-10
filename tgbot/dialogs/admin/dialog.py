from aiogram.types import ContentType
from aiogram_dialog import Dialog,  Window
from aiogram_dialog.widgets.kbd import (
    Row, SwitchTo, Column,
    Group, Cancel, Button, Back
)
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import DynamicMedia


from tgbot.dialogs.states import Menu, PrizeDraw, AdminPanel
from tgbot.dialogs.getters import username_getter, object_bot, get_giveaway_settings
from tgbot.dialogs.admin.callback import (
    on_export_participants,
    winner_message,
    on_settings,
    on_set_giveaway_text,
    on_set_giveaway_image,
    on_set_channel_id
)


admin_panel = Dialog(
    Window(
        Const(text='Выбери действие'),
        Group(
            Row(
                SwitchTo(
                    Const(text='Отправить сообщение о выйгрыше'),
                    id='start_draw',
                    state=AdminPanel.Prize
                ),
                Button(
                    Const("Настройка розыгрыша"),
                    id="settings",
                    on_click=on_settings
                )

            ),
            Column(
                Button(
                    Const("Экспорт участников"),
                    id="export",
                    on_click=on_export_participants),
            )
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
    Window(
        Const("Настройки розыгрыша"),
        DynamicMedia(
            selector="photo",
            when="photo",
        ),
        Format("Текущий текст розыгрыша: {current_text}"),
        Format("Текущий ID канала: {current_channel_id}"),
        Group(
            Row(
                SwitchTo(
                    Const("Изменить текст"),
                    id="set_text",
                    state=AdminPanel.SetGiveawayText
                ),
                SwitchTo(
                    Const("Изменить изображение"),
                    id="set_image",
                    state=AdminPanel.SetGiveawayImage
                ),
            ),
            Row(
                SwitchTo(
                    Const("Изменить ID канала"),
                    id="set_channel",
                    state=AdminPanel.SetChannelId
                ),
            )
        ),
        Column(
            SwitchTo(
                Const('◀️ Назад'),
                id='back_to_admin',
                state=AdminPanel.Start
            ),
        ),
        getter=get_giveaway_settings,
        state=AdminPanel.GiveawaySettings
    ),
    Window(
        Const("Введите новый текст для розыгрыша:"),
        MessageInput(
            func=on_set_giveaway_text,
            content_types=ContentType.TEXT
        ),
        SwitchTo(
            Const('◀️ Назад'),
            id='back',
            state=AdminPanel.GiveawaySettings
        ),
        state=AdminPanel.SetGiveawayText
    ),
    Window(
        Const("Отправьте новое изображение для розыгрыша:"),
        MessageInput(
            func=on_set_giveaway_image,
            content_types=ContentType.PHOTO
        ),
        SwitchTo(
            Const('◀️ Назад'),
            id='back',
            state=AdminPanel.GiveawaySettings
        ),
        state=AdminPanel.SetGiveawayImage
    ),
    Window(
        Const("Введите ID канала для проверки подписки (@channel_name или -100...):"),
        MessageInput(
            func=on_set_channel_id,
            content_types=ContentType.TEXT
        ),
        Back(
            Const('◀️ Назад'),
            id='back',
        ),
        state=AdminPanel.SetChannelId
    )
)
