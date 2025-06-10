from aiogram.types import ContentType
from aiogram import F, Router
from aiogram.filters import Command
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, Cancel, Back
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media import DynamicMedia

from tgbot.dialogs.giveaway.callback import on_subscription_check, process_screenshot
from tgbot.dialogs.states import GiveawayDialog
from tgbot.dialogs.getters import get_giveaway_data


giveaway_dialog = Dialog(
    Window(
        Format(
            "{giveaway_welcome}",
            when="ready_to_giveaway"
        ),
        Button(
            Format("{giveaway_start}"),
            id="check_subscription",
            when="ready_to_giveaway",
            on_click=on_subscription_check
        ),
        Format("{giveaway_already_participated}",
               when="not_ready_to_giveaway"),
        Cancel(
            Format("{btn_back}")
        ),
        state=GiveawayDialog.Start,
        getter=get_giveaway_data,
    ),
    Window(
        Format("{giveaway_screenshot_request}"),
        MessageInput(
            process_screenshot,
            content_types=ContentType.PHOTO
        ),
        Back(
            Format("{btn_back}")
        ),
        state=GiveawayDialog.ScreenshotUpload,
        getter=get_giveaway_data,
    ),
    Window(
        Format("{giveaway_thanks}"),
        Format("{giveaway_follow_up}"),
        Cancel(
            Format("{btn_back}"),
        ),
        state=GiveawayDialog.Participation,
    ),
    getter=get_giveaway_data
)
