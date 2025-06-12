from aiogram.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    Start = State()
    help = State()


class AdminPanel(StatesGroup):
    Start = State()
    EnterWinner = State()
    Prize = State()
    GiveawaySettings = State()
    SetGiveawayText = State()
    SetGiveawayImage = State()
    SetChannelId = State()


class GiveawayDialog(StatesGroup):
    """Состояния для диалога розыгрыша"""
    start = State()
    subscription_check = State()
    screenshot_upload = State()
    screenshot_verification = State()
    wait_for_desicion = State()
