from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import Config

# для хранения
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# создаём экземпляр класса
storage = MemoryStorage()
bot = Bot(token=Config.token)
# передаём экземпляр диспетчеру
dp = Dispatcher(bot, storage=storage)