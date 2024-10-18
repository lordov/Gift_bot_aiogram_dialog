from aiogram.types import ContentType
from aiogram_dialog import Dialog,  Window
from aiogram_dialog.widgets.kbd import (
    Button, Back, Url
)
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from tgbot.dialogs.states import BroadcastPanel
from tgbot.dialogs.broadcast_dialog.broadcast_callback import (
    on_confirm, on_message_input, on_photo_input, on_url_input)
from tgbot.dialogs.getters import get_full_post


broadcast_dialog = Dialog(
    Window(
        Const("Введите текст для рассылки:"),
        MessageInput(
            func=on_message_input,
            content_types=ContentType.TEXT
        ),
        state=BroadcastPanel.Text,
    ),
    Window(
        Const("Отправьте фото"),
        MessageInput(
            func=on_photo_input,
            content_types=ContentType.PHOTO
        ),
        Back(Const("Назад")),
        state=BroadcastPanel.Photo,
    ),
    Window(
        Const("Введите URL для кнопки"),
        MessageInput(
            func=on_url_input,
            content_types=ContentType.TEXT
        ),
        Back(Const("Назад")),
        state=BroadcastPanel.Url,
    ),
    Window(
        Format(
            "Проверьте сообщение:\n\n{text}"
        ),
        StaticMedia(
            url=Format('{photo}'),
        ),
        Url(
            text=Const("Перейти"),
            url=Format('{url}'),
            when='url'),
        Button(Const("Отправить"), id="confirm", on_click=on_confirm),
        Back(Const("Назад")),
        getter=get_full_post,
        state=BroadcastPanel.Confirm,
    ),
)
