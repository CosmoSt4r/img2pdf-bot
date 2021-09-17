"""Module for storing states for bot."""

from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    """States for aiogram state machine."""

    photos = State()
    name = State()
