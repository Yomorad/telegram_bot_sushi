from aiogram.utils import executor
from create_bot import dp
from database import sqlrequests
from handlers import client, admin
import middlewares

middlewares.setup(dp)

async def on_startup(_):
    print ("Бот вышел в онлайн")
    # управляю миграциями через alembic, но на всякий случай оставлю заглушку если потребуется
    # models.Base.metadata.create_all(bind=engine)
    # print("База данных создана")
    if not await sqlrequests.sql_read_restaurant_for_availability():
        sqlrequests.sql_try_fixtures()
    print("Фикстуры загружены")

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)