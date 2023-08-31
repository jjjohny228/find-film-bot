from create_bot import bot
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from create_bot import check_sub_channels
from config import NOT_SUB_MESSAGE
import datetime
from statistics import get_today_statistics, get_month_statistics, get_all_time_statistics
from keyboards.all_keyboards import *
from data_base import data_functions
from aiogram.types import InputFile


class FilmsStateGroup(StatesGroup):
    title = State()
    photo = State()
    url = State()


class FindFilmStateGroup(StatesGroup):
    title = State()


async def delete_film_instruction(message: types.Message):
    await bot.send_message(message.from_user.id,
                           text="Чтобы удалить фильм напишите: 'Удалить <номер фильма>'",
                           reply_markup=get_back_admin_keyboard())


async def back_main_menu(message: types.Message, state: FSMContext):
    if state is None:
        await message.answer('🏠', reply_markup=get_admin_keyboard())
        return
    await state.finish()
    await message.answer('🏠', reply_markup=get_admin_keyboard())


async def find_film_number(message: types.Message):
    await message.answer(text="Введите <Название фильма> (<год>)'",
                         reply_markup=get_cancel_search_keyboard())
    await FindFilmStateGroup.title.set()


async def cancel_search(message: types.Message, state: FSMContext):
    if state is None:
        await message.reply("Успешная отмена", reply_markup=get_admin_keyboard())
        return
    await state.finish()
    await message.reply("Успешная отмена", reply_markup=get_admin_keyboard())


async def find_film_id(message: types.Message, state: FSMContext):
    find_film = await data_functions.show_film_id(message.text)
    if find_film is None:
        await message.answer("Такого фильма в бд нет\n"
                             "Или ввод некоректен")
    else:
        await message.answer(f"Номер Вашего фильма: {find_film}")
    await state.finish()


async def display_all_films(message: types.Message):
    result = "\n".join(str(film[0])+' '+film[1] for film in await data_functions.show_all_films())
    await message.answer(result)


async def statistic_menu(message: types.Message):
    await message.answer("Статистика посещаемости", reply_markup=get_statistic_keyboard())


async def today_statistic(message: types.Message):
    await message.answer(await get_today_statistics())


async def month_statistic(message: types.Message):
    await message.answer(await get_month_statistics())


async def all_time_statistic(message: types.Message):
    await message.answer(await get_all_time_statistics())


async def delete_film(message: types.Message):
    if message.from_user.id == 617073201:
        if message.text.count(' ') != 1:
            await message.answer("Ввод некоректен")
        else:
            film_number = message.text.split()[1]
            film_delete_verification = await data_functions.show_film_title(film_number)
            await bot.send_message(message.from_user.id, "Этот фильм Вы хотите удалить?")
            await bot.send_message(message.from_user.id,
                                   text=film_delete_verification[0],
                                   reply_markup=get_delete_keyboard())
    else:
        await message.answer("Вы не можете удалить фильм. Вы не владелец бота!")


async def del_film(callback: types.CallbackQuery):
    if callback.data == "time_delete":
        await data_functions.delete_film(callback.message.text)
        await bot.send_message(callback.from_user.id,
                               text="Фильм был успешно удален",
                               reply_markup=get_admin_keyboard())
    else:
        await bot.send_message(callback.from_user.id, "Фильм не был удален", reply_markup=get_admin_keyboard())


async def subscribed_result(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    if await check_sub_channels(CHANNELS, callback.from_user.id):
        await bot.send_message(callback.from_user.id, text="<em>Доступ к базе данных открыт</em>", parse_mode="HTML")
        await data_functions.add_user(callback.from_user.id, datetime.datetime.now())

        await bot.send_message(chat_id=callback.from_user.id,
                               text="Нажмите кнопку <b>Найти фильм</b>🔎",
                               parse_mode="HTML",
                               reply_markup=get_search_keyboard())
    else:
        await bot.send_message(callback.from_user.id, NOT_SUB_MESSAGE, reply_markup=show_channels_keyboard())


async def cancel_function(message: types.Message, state: FSMContext):
    if state is None:
        await message.reply("Вы успешно прервали загрузку фильма", reply_markup=get_admin_keyboard())
        return
    await state.finish()
    await message.reply("Вы успешно прервали загрузку фильма", reply_markup=get_admin_keyboard())


async def add_film(message: types.Message):
    await bot.send_message(message.from_user.id,
                           text="Напишите название фильма с годом",
                           reply_markup=get_cancel_keyboard()
                           )
    await FilmsStateGroup.title.set()


async def add_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["title"] = message.text
    await bot.send_message(message.from_user.id, "Теперь загрузите ссылку на фото")
    await FilmsStateGroup.next()


async def load_photo(message: types.Message, state: FSMContext):
    print(message.photo)
    async with state.proxy() as data:
        data['photo'] = str(message.text)
    await bot.send_message(message.from_user.id, "Дальше загрузите ссылку на фильм")
    await FilmsStateGroup.next()


# async def invalid_photo(message: types.Message):
#     await message.reply("Вы отправили не фото")


async def load_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url'] = str(message.text)
    await data_functions.add_film(data)
    await state.finish()
    await bot.send_message(message.from_user.id, "Фильм был успешно загружен")
    await bot.send_message(message.from_user.id,
                           text=f"Номер фильма, который сейчас был загружен: {await data_functions.show_last_film_id()}",
                           reply_markup=get_admin_keyboard())


async def download_data_base_command(message: types.Message):
    await bot.send_document(message.from_user.id, InputFile('main_data_base.db'))


def register_admin_handlers(disp: Dispatcher):
    disp.register_message_handler(delete_film_instruction, Text("Удалить фильм🗑"))
    disp.register_message_handler(back_main_menu, Text("Главное меню"), state='*')
    disp.register_message_handler(find_film_number, Text("Номер фильма🔎"))
    disp.register_message_handler(cancel_search, Text("Отмена поиска"), state='*')
    disp.register_message_handler(find_film_id, state=FindFilmStateGroup.title)
    disp.register_message_handler(display_all_films, Text("Список всех фильмов🍿"))
    disp.register_message_handler(statistic_menu, Text("Посещаемость👶"))
    disp.register_message_handler(today_statistic, Text("День"))
    disp.register_message_handler(month_statistic, Text("Месяц"))
    disp.register_message_handler(all_time_statistic, Text("Все время"))
    disp.register_message_handler(delete_film, lambda text: text.text.startswith("Удалить"))
    disp.register_callback_query_handler(del_film, lambda text: text.data.endswith('delete'))
    disp.register_callback_query_handler(subscribed_result, text="subscribed")

    disp.register_message_handler(cancel_function, Text("Отмена"), state='*')
    disp.register_message_handler(add_film, Text("Добавить фильм🎥"))
    disp.register_message_handler(add_title, state=FilmsStateGroup.title)
    disp.register_message_handler(load_photo, state=FilmsStateGroup.photo)
    # disp.register_message_handler(invalid_photo, lambda message: not message.photo, state=FilmsStateGroup.photo)
    disp.register_message_handler(load_url, state=FilmsStateGroup.url)
    disp.register_message_handler(download_data_base_command, Text("Скачать бд🗂️"))
