from aiogram.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    start = State()
    help_rich_cat = State()
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
