"""Module for message handlers."""

from aiogram import types
from aiogram.dispatcher import FSMContext

from modules.bot import dp
from modules.states import States


@dp.message_handler(state='*', commands=['start'])
async def process_start(msg: types.Message, state: FSMContext):
    """
    Process /start command.

    Args:
        msg: message from user
        state: aiogram State
    """
    await state.finish()

    message = (
        'Добро пожаловать!',
        'Я помогу вам собрать PDF файл из фотографий.',
        'Введите /upload, чтобы начать.',
    )
    await msg.reply(' '.join(message), reply=False)


@dp.message_handler(state=States.uploading, commands=['upload'])
async def process_upload_uploading(msg: types.Message):
    """
    Process /upload command when state is 'uploading'.

    Args:
        msg: message from user
    """
    message = (
        'Вы уже загружаете фотографии.',
        'Введите /stop, чтобы сформировать PDF файл.',
    )
    await msg.reply(' '.join(message), reply=False)


@dp.message_handler(state=States.uploading)
async def process_text_uploading(msg: types.Message):
    """
    Process text any text messages when state is 'uploading'.

    Args:
        msg: message from user
    """
    message = (
        'В данный момент вы загружаете фото.',
        'Введите /stop, чтобы сформировать PDF файл.',
    )
    await msg.reply(' '.join(message), reply=False)


@dp.message_handler(state='*', commands=['upload'])
async def process_upload(msg: types.Message):
    """
    Process /upload command.

    Args:
        msg: message from user
    """
    message = (
        'Отправляйте мне фотографии.',
        'Чтобы закончить, введите /stop.',
    )
    await States.uploading.set()
    await msg.reply(' '.join(message), reply=False)


@dp.message_handler(state='*')
async def process_text(msg: types.Message):
    """
    Process text any text messages.

    Args:
        msg: message from user
    """
    message = 'Для начала загрузки фото введите /upload'
    await msg.reply(message, reply=False)
