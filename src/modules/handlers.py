"""Module for message handlers."""

from aiogram import types
from bot import bot, dp


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    """
    Process /start command from user.

    Args:
        msg: message from user
    """
    await msg.reply('Привет!\nНапиши мне что-нибудь!')


@dp.message_handler()
async def process_text_message(msg: types.Message):
    """
    Process any text message from user.

    Args:
        msg: message from user
    """
    await bot.send_message(msg.from_user.id, msg.text)
