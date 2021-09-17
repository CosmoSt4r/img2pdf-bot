"""Module for message handlers."""

from aiogram import types
from aiogram.dispatcher import FSMContext

from modules.bot import bot, dp
from modules.files import delete_files
from modules.img2pdf import generate_pdf
from modules.states import States


@dp.message_handler(state='*', commands=['start'])
async def process_start(msg: types.Message, state: FSMContext):
    """
    Process /start command.

    Args:
        msg: message from user
        state: current state
    """
    await state.finish()

    message = (
        'Добро пожаловать!',
        'Я помогу вам собрать PDF файл из фотографий.',
        'Введите /upload, чтобы начать.',
        )
    await msg.reply(' '.join(message), reply=False)


@dp.message_handler(state=States.photos, commands=['upload'])
async def process_already_uploading(msg: types.Message):
    """
    Process /upload command when state is 'photos'.

    Args:
        msg: message from user
    """
    message = (
        'Вы уже загружаете фотографии.',
        'Введите /stop, чтобы сформировать PDF файл.',
        )
    await msg.reply(' '.join(message), reply=False)


@dp.message_handler(state=States.photos, commands=['stop'])
async def process_stop_uploading(msg: types.Message, state: FSMContext):
    """
    Process /stop command when state is 'photos'.

    Args:
        msg: message from user
        state: current state
    """
    async with state.proxy() as pdf:
        photos_count = len(pdf.setdefault('photos', []))

    if photos_count:
        await States.next()
        message = (
            'Фотографий получено: {0}'.format(photos_count),
            '\nВведите название PDF файла.',
        )
    else:
        await state.finish()
        message = (
            'Вы не загрузили фотографии.',
            '\nВведите /upload для повтора.',
        )

    await msg.reply(' '.join(message), reply=False)


@dp.message_handler(state=States.photos, content_types=['photo'])
async def process_photo_uploading(msg: types.Message, state: FSMContext):
    """
    Process photo upload when state is 'photos'.

    Args:
        msg: message from user
        state: current state
    """
    async with state.proxy() as pdf:
        pdf.setdefault('photos', []).append(msg.photo[-1].file_id)


@dp.message_handler(state=States.photos)
async def process_text_uploading(msg: types.Message):
    """
    Process text any text messages when state is 'photos'.

    Args:
        msg: message from user
    """
    message = (
        'В данный момент вы загружаете фото.',
        'Введите /stop, чтобы сформировать PDF файл.',
        )
    await msg.reply(' '.join(message), reply=False)


@dp.message_handler(state=States.name)
async def process_file_name(msg: types.Message, state: FSMContext):
    """
    Process text any text messages when state is 'name'.

    Args:
        msg: message from user
        state: current state
    """
    await msg.reply('Формирую PDF файл...', reply=False)
    
    async with state.proxy() as pdf:
        pdf['name'] = 'media/{0}'.format(msg.text)

        photos = []
        for photo_id in pdf['photos']:
            filepath = 'media/{0}.jpg'.format(photo_id)
            await bot.download_file_by_id(photo_id, filepath)
            photos.append(filepath)

        pdf_file_name = generate_pdf(photos, pdf['name'])
        await bot.send_document(msg.from_user.id, open(pdf_file_name, 'rb'))
    
    await state.finish()
    await delete_files(photos + [pdf_file_name])


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
    await States.photos.set()
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
