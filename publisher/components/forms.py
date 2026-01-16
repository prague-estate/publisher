"""Bot forms and states."""

from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    """Change filters states."""

    max_price = State()
    min_price = State()
    min_usable_area = State()
