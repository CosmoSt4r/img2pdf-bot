"""Module for message handlers."""

from aiogram import types

from modules.bot import dp
from modules.states import States


@dp.message_handler(state='*', commands=['start'])
async def process_start_command(msg: types.Message):
    """
    Process /start command from user.

    Args:
        msg: message from user
    """
    state = dp.current_state(user=msg.from_user.id)
    await state.reset_state()

    message = """Добро пожаловать!
    Я помогу вам собрать PDF файл из фотографий.
    Введите /upload, чтобы начать."""
    await msg.reply(message, reply=False)


@dp.message_handler(state='*')
async def process_text_message(msg: types.Message):
    """
    Process text any text messages .

    Args:
        msg: message from user
    """
    state = dp.current_state(user=msg.from_user.id)

    if state == States.uploading:
        message = """В данный момент вы загружаете фото.
        Введите /stop, чтобы сформировать PDF файл."""
    else:
        message = 'Для начала загрузки фото введите /upload'
    await msg.reply(message, reply=False)
