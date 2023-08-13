import datetime
import pytz
from data_base import data_functions


async def get_today_statistics() -> str:
    result_users = await data_functions.show_today_users()
    result_started_users = await data_functions.show_today_started_users()
    return f"Новых пользователей за день: {await is_none_or_not(result_users)}\n\n" \
           f"Стартующих за день: {await is_none_or_not(result_started_users)}"


async def get_month_statistics() -> str:
    now = get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    result_users = await data_functions.show_month_users(first_day_of_month)
    result_started_users = await data_functions.show_month_started_users(first_day_of_month)
    return f"Новых пользователей за месяц: {await is_none_or_not(result_users)}\n\n" \
           f"Стартующих за месяц: {await is_none_or_not(result_started_users)}"


def get_now_datetime():
    tz = pytz.timezone("Europe/Kiev")
    now = datetime.datetime.now(tz)
    return now


async def get_all_time_statistics():
    result_users = await data_functions.show_all_time_users()
    result_started_users = await data_functions.show_all_time_started_users()
    return f"Новых пользователей за все время: {await is_none_or_not(result_users)}\n\n" \
           f"Стартующих за все время: {await is_none_or_not(result_started_users)}"


def get_now_formatted():
    return get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


async def is_none_or_not(data_result):
    if data_result is None:
        return 0
    else:
        return data_result[0]