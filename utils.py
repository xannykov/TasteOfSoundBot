import telebot, io, requests
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from yandex_music import Client

bot = telebot.TeleBot('TOKEN')
client = Client('TOKEN').init()