"""Main file to run bot."""

from aiogram.utils import executor

from modules.handlers import dp

if __name__ == '__main__':
    executor.start_polling(dp)
