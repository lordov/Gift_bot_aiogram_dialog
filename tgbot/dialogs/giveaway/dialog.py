from aiogram.types import ContentType
from aiogram import F, Router
from aiogram.filters import Command
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media import DynamicMedia

from tgbot.dialogs.giveaway.callback import on_subscription_check, process_screenshot
from tgbot.dialogs.states import GiveawayDialog
from tgbot.dialogs.getters import get_giveaway_data


giveaway_dialog = Dialog(
    Window(
        Format("Добро пожаловать в розыгрыш LaKarti!"),
        DynamicMedia(
            get_giveaway_data,
            when=F["giveaway_settings"].image_path
        ),
        Format("{giveaway_settings.text}"),
        Button(
            Const("Участвовать"),
            id="check_subscription",
            on_click=on_subscription_check
        ),
        Cancel(
            Const("Отмена")
        ),
        state=GiveawayDialog.Start,
        getter=get_giveaway_data,
    ),
    Window(
        Const("Пожалуйста, отправьте скриншот с датой покупки из личного кабинета WB или OZON."),
        MessageInput(
            process_screenshot,
            content_types=ContentType.PHOTO
        ),
        Cancel(Const("Отмена")),
        state=GiveawayDialog.ScreenshotUpload,
    ),
    Window(
        Format("Спасибо! Ваш номер для участия: {participation_number}"),
        Format("О дате розыгрыша и результатах будем сообщать в Telegram-канале Lakarti - искусство в твоем доме https://t.me/lakartiphoto. Оставайтесь с нами!"),
        Button(
            Const("Закрыть"), id="close",
            on_click=lambda c, b, dm: dm.done()
        ),
        state=GiveawayDialog.Participation,
    ),
    Window(
        Const("Вы уже принимали участие в розыгрыше в этом месяце."),
        Button(
            Const("Закрыть"),
            id="close",
            on_click=lambda c, b, dm: dm.done()
        ),
        state=GiveawayDialog.AlreadyParticipated,
    ),
)
