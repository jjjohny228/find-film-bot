import datetime

from aiogram import types, Dispatcher
from create_bot import bot, check_sub_channels
from aiogram.dispatcher.filters import Text
from config import CHANNELS, NOT_SUB_MESSAGE
from keyboards.all_keyboards import show_channels_keyboard, get_film_keyboard, get_admin_keyboard, get_search_keyboard
from data_base import data_functions


# @dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await data_functions.add_started_users(message.from_user.id, datetime.datetime.now())
    if message.from_user.id == 617073201:
        await message.answer("Добро пожаловать хозяин", reply_markup=get_admin_keyboard())
    else:
        if await check_sub_channels(CHANNELS, message.from_user.id):
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Нажмите кнопку <b>Найти фильм</b>🔎",
                                   parse_mode="HTML",
                                   reply_markup=get_search_keyboard())
        else:
            await bot.send_message(message.from_user.id, NOT_SUB_MESSAGE, reply_markup=show_channels_keyboard())
            await bot.send_message(message.from_user.id,
                                   text="<em>После подписки, обязательно нажмите\n\n«Я подписался✅»\n\n"
                                        "Доступ к базе данных фильмов в боте будет открыт автоматически.</em>\n\n"
                                        "<b>Внимание!</b> Код нужно вводить в боте.", parse_mode="HTML")


# @dp.message_handler(Text("Найти фильм🔎"))
async def first_search_film(message: types.Message):
    await bot.send_message(message.from_user.id,
                           text="Введите код фильма🍿\n\nТолько цифры‼️")


# @dp.message_handler() #проверка подписки на все каналы
async def show_film(message: types.Message):
    if await check_sub_channels(CHANNELS, message.from_user.id):
        if not message.text.isdigit():
            await bot.send_message(message.from_user.id, "Вы ввели не код. \nПопробуйте еще раз")
        else:
            film_chosen = await data_functions.show_film_info(int(message.text))
            if film_chosen is None:
                await bot.send_message(message.from_user.id,
                                       text="<b>Фильм с таким кодом не существует.</b>\n\nВведите коректный код.",
                                       parse_mode="HTML")
            else:
                await bot.send_photo(message.from_user.id,
                                     photo=film_chosen[2],
                                     caption=film_chosen[1],
                                     reply_markup=get_film_keyboard(film_chosen[3]))
    else:
        await bot.send_message(message.from_user.id, NOT_SUB_MESSAGE, reply_markup=show_channels_keyboard())


def register_client_handlers(disp: Dispatcher):
    disp.register_message_handler(start_command, commands=['start'])
    disp.register_message_handler(first_search_film, Text("Найти фильм🔎"))
    disp.register_message_handler(show_film)

