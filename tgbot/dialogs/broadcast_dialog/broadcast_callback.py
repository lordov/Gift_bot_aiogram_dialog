from tkinter import Button
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram_dialog import DialogManager
from nats.js.client import JetStreamContext
from tgbot.services.broadcast_service.publisher import publish_broadcast_message


async def on_message_input(message: Message, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(text=message.text)
    await dialog_manager.next()


async def on_photo_input(message: Message, button: Button, dialog_manager: DialogManager):
    post_photo = message.photo[-1].file_id
    dialog_manager.dialog_data.update(photo=post_photo)
    await dialog_manager.next()


async def on_url_input(message: Message, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(url=message.text)
    await dialog_manager.next()


async def on_confirm(
        callback: CallbackQuery, 
        button: Button, 
        dialog_manager: DialogManager,

):
    # Здесь будем публиковать сообщение в JetStream
    data = dialog_manager.current_context().dialog_data
    js: JetStreamContext = dialog_manager.middleware_data.get('js')
    broadcast_subject = dialog_manager.middleware_data.get('broadcast_subject')
    # Вызовем функцию для публикации
    await publish_broadcast_message(
        js=js,
        message_data=data,
        subject=broadcast_subject
        )
    await callback.message.answer("Рассылка запущена!")
    await dialog_manager.done()
