from aiogram.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    Start = State()
    help = State()
    product_size = State()
    product_60_120 = State()
    product_75_150 = State()
    Url_60_120 = State()
    Url_75_150 = State()


class PrizeDraw(StatesGroup):
    prize_condition = State()
    help_for_review = State()
    review_screenshot = State()
    purchase_screenshot = State()
    finish = State()


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


class GiveawayAdminPanel(StatesGroup):
    """Состояния для административной панели розыгрыша"""
    Start = State()
    SetGiveawayText = State()
    SetGiveawayImage = State()
    ExportParticipants = State()
    ManageGiveaway = State()
