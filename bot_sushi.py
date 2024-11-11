from aiogram.utils import executor
from create_bot import dp
from database import sqlrequests
from handlers import client, admin
import middlewares

middlewares.setup(dp)

async def on_startup(_):
    print ("Бот вышел в онлайн")
    sqlrequests.sql_start()
    if await sqlrequests.sql_read_restaurant_for_availability():
        await sqlrequests.sql_add_start_date()

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)