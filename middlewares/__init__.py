from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware

from .throttling import rate_limit

def setup (dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())