
from aiogram.dispatcher.filters.state import State, StatesGroup


class Info(StatesGroup):
    video = State()
    channel = State()
    channel_yadisk = State()
    answer = State()