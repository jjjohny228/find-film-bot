from aiogram import executor
from create_bot import dp
from handlers.admin import register_admin_handlers
from handlers.client import register_client_handlers
from data_base.data_functions import start_db


async def on_startup(_):
    print("Бот был запущен")
    await start_db()

register_admin_handlers(dp)
register_client_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
