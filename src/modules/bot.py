"""Module for storing Telegram bot."""

import os

import telebot

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
