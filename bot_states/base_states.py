from aiogram.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    start = State()
    product = State()
    product_size = State()
    product_60_120 = State()
    product_75_150 = State()
    gift_condition = State()


class ScreenshotsState(StatesGroup):
    review_screenshot = State()
    purchase_screenshot = State()
    verification = State()
