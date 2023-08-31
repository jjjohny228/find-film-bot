from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import CHANNELS


def show_channels_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)

    for chanel_number in range(len(CHANNELS)):
        button = InlineKeyboardButton(text=CHANNELS[chanel_number][0],
                                      url=CHANNELS[chanel_number][2])
        keyboard.insert(button)

    button_success_sub = InlineKeyboardButton("Я подписался✅", callback_data='subscribed')
    keyboard.insert(button_success_sub)
    return keyboard


def get_search_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = KeyboardButton("Найти фильм🔎")
    keyboard.add(btn)
    return keyboard


def get_admin_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Добавить фильм🎥")
    btn2 = KeyboardButton("Удалить фильм🗑")
    btn3 = KeyboardButton("Номер фильма🔎")
    btn4 = KeyboardButton("Посещаемость👶")
    btn5 = KeyboardButton("Список всех фильмов🍿")
    btn6 = KeyboardButton("Скачать бд🗂️")
    keyboard.add(btn1, btn2).add(btn3, btn4).add(btn5, btn6)
    return keyboard


def get_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Отмена")
    btn2 = KeyboardButton("Главное меню")
    keyboard.add(btn1).add(btn2)
    return keyboard


def get_delete_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton("ДА✅", callback_data='time_delete'),
         InlineKeyboardButton("Нет🚫", callback_data='not_time_delete')]
    ])
    return keyboard


def get_back_admin_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("Главное меню")
    keyboard.add(btn)
    return keyboard


def get_film_keyboard(url):
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn = InlineKeyboardButton("👀 СМОТРЕТЬ", url=url)
    keyboard.add(btn)
    return keyboard


def get_statistic_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("День")
    btn2 = KeyboardButton("Месяц")
    btn3 = KeyboardButton("Все время")
    btn4 = KeyboardButton("Главное меню")
    keyboard.add(btn1).add(btn2).add(btn3).add(btn4)
    return keyboard


def get_cancel_search_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Отмена поиска")
    btn2 = KeyboardButton("Главное меню")
    keyboard.add(btn1).add(btn2)
    return keyboard
