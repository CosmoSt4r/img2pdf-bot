"""Module for message handlers."""

from modules.bot import bot, telebot


@bot.message_handler(commands=['start'])
def handle_start_command(message: telebot.types.Message):
    """
    Handle /start command.

    Args:
        message: message from user

    Returns:
        greeting message
    """
    reply: str = 'Добро пожаловать!'

    return bot.send_message(message.from_user.id, reply)
