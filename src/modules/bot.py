"""Module for storing Telegram bot."""

import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher

bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher(bot)
