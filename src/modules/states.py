"""Module for storing states for bot."""

from aiogram.utils.helper import Helper, HelperMode, Item


class States(Helper):
    """States for aiogram state machine."""

    mode = HelperMode.snake_case

    uploading = Item()
