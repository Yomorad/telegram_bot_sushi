from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from keyboards import client_kb
from data_base import postgres_db
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,LabeledPrice, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import Config
import datetime, random, pytz

from middlewares import rate_limit

class FSMclient(StatesGroup):
    name_c = State()
    number_c = State()
    adress_c = State()
    adress_c_1 = State()
    commentary_c = State()
    tools_c = State()
    time_order_c = State()

@rate_limit(limit=5, key = '/start')
#@dp.message_handler(commands=['start'])
async def commands_start(message: types.Message):
    try:
        mess = f'😃 Благодарим, что присоединились к нам!' \
               f'\n Вас ждет:' \
               f'\n 👍 - наивкуснейшие суши и роллы' \
               f'\n 👍 - быстрая доставка' \
               f'\n 👍 - приветливый персонал и комфортное обслуживание!' \
               f'\n 👇 Ознакомьтесь с нашим меню!'
        await postgres_db.sql_start2(message)
        await message.bot.send_message(message.from_user.id, mess, reply_markup=client_kb.kb_client)
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему \nhttps://t.me/Sushi_for_everybody_bot')
        await message.bot.send_message(message.from_user.id, f'Здравствуйте!' , reply_markup=client_kb.kb_client)

@rate_limit(limit=5, key = '👨‍🍳 Информация о заведении')
#@dp.message_handler(text='👨‍🍳 Информация о заведении')
async def commands_location(message: types.Message):
    await postgres_db.sql_read_restaurant(message)

'''*****************************************Логика меню*************************************************'''
cb = CallbackData('btn', 'type', 'product_id', 'category_id')

# вывод генератора клавиатуры с товарами
async def gen_products(data, user_id):
    keyboard = InlineKeyboardMarkup()
    for i in data:
        count = await postgres_db.get_count_in_cart(user_id, i[1])
        count = 0 if not count else sum(j[0] for j in count)
        keyboard.add(InlineKeyboardButton(text=f'{i[3]}: {i[5]}p - {count}шт', callback_data=f'btn:plus:{i[1]}:{i[6]}'))
        keyboard.add(InlineKeyboardButton(text='🔽 Убавить' , callback_data=f'btn:minus:{i[1]}:{i[6]}'),
                     InlineKeyboardButton(text='🔼 Добавить', callback_data=f'btn:plus:{i[1]}:{i[6]}'),
                     InlineKeyboardButton(text='❌ Очистить', callback_data=f'btn:del:{i[1]}:{i[6]}'))
    return keyboard

@rate_limit(limit=5, key = '🍰 Меню')
#@dp.message_handler(text='🍰 Меню')
async def commands_products(message: types.Message):
    for ret in await postgres_db.sql_read_restaurant_for_availability():
        prov_availability = f'{ret[6]}'
        mess_availability = f'{ret [7]}'
    if str(prov_availability) == '1':
        data = await postgres_db.get_categories()
        keyboard = InlineKeyboardMarkup()
        for i in data:
            keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'btn:category:-:{i[1]}'))
        await message.answer('Ознакомьтесь с нашим меню', reply_markup=keyboard)
    else:
        await message.answer(mess_availability)

@dp.callback_query_handler(cb.filter(type='category'))
async def goods(callback_query: types.CallbackQuery, callback_data: dict):
    data = await postgres_db.get_products(callback_data.get('category_id'))
    for ret in data:
        count = await postgres_db.get_count_in_cart(callback_query.message.chat.id, ret[1])
        count = 0 if not count else sum(j[0] for j in count)
        k1 = InlineKeyboardButton(text=f'{ret[3]}: {ret[5]}p - {count}шт', callback_data=f'btn:plus:{ret[1]}:{ret[6]}')
        k2 = InlineKeyboardButton(text='🔽 Убавить' , callback_data=f'btn:minus:{ret[1]}:{ret[6]}')
        k3 = InlineKeyboardButton(text='🔼 Добавить', callback_data=f'btn:plus:{ret[1]}:{ret[6]}')
        k4 = InlineKeyboardButton(text='❌ Очистить', callback_data=f'btn:del:{ret[1]}:{ret[6]}')
        inkb_main = InlineKeyboardMarkup(resize_keyboard=True)
        inkb_main.add(k1).add(k2, k3, k4)
        await bot.send_photo(callback_query.message.chat.id, ret[2], f'{ret[3]}\n{ret[4]}',reply_markup=inkb_main)
    await bot.send_message(callback_query.message.chat.id, 'Посмотрите другие категории!', reply_markup=InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Назад', callback_data=f'btn:back:-:-')))

@dp.callback_query_handler(cb.filter(type='back'))
async def back(callback_query: types.CallbackQuery):
    data = await postgres_db.get_categories()
    keyboard = InlineKeyboardMarkup()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'btn:category:-:{i[1]}'))
    await callback_query.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(cb.filter(type='minus'))
async def minus(callback_query: types.CallbackQuery, callback_data: dict):
    product_id = callback_data.get('product_id')
    count_in_cart = await postgres_db.get_count_in_cart(callback_query.message.chat.id, product_id)
    if not count_in_cart or count_in_cart[0][0] == 0:
        await callback_query.message.answer('Товар в  корзине отсутсвует!')
        return 0
    elif count_in_cart[0][0] == 1:
        await postgres_db.remove_one_item(product_id, callback_query.message.chat.id)
    else:
        await postgres_db.change_count(count_in_cart[0][0] - 1, product_id, callback_query.message.chat.id)
    data = await postgres_db.get_products_1(callback_data.get('category_id'), callback_data.get('product_id'))
    keyboard = await gen_products(data, callback_query.message.chat.id)
    await callback_query.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(cb.filter(type='plus'))
async def plus(callback_query: types.CallbackQuery, callback_data: dict):
    product_id = callback_data.get('product_id')
    count_in_cart = await postgres_db.get_count_in_cart(callback_query.message.chat.id, product_id)
    if not count_in_cart or count_in_cart[0][0] == 0:
        await postgres_db.add_to_cart(callback_query.message.chat.id, product_id)
        await callback_query.message.answer('Добавил!')
    else:
        await postgres_db.change_count(count_in_cart[0][0] + 1, product_id, callback_query.message.chat.id)
    data = await postgres_db.get_products_1(callback_data.get('category_id'), callback_data.get('product_id'))
    keyboard = await gen_products(data, callback_query.message.chat.id)
    await callback_query.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(cb.filter(type='del'))
async def delete(callback_query: types.CallbackQuery, callback_data: dict):
    product_id = callback_data.get('product_id')
    count_in_cart = await postgres_db.get_count_in_cart(callback_query.message.chat.id, product_id)
    if not count_in_cart:
        await callback_query.message.answer('Товар в корзине отсутствует!')
        return 0
    else:
        await postgres_db.remove_one_item(product_id, callback_query.message.chat.id)
    data = await postgres_db.get_products_1(callback_data.get('category_id'), callback_data.get('product_id'))
    keyboard = await gen_products(data, callback_query.message.chat.id)
    await callback_query.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Очистить корзину'))
@dp.message_handler(text='Очистить корзину')
async def empty_cart(message: types.Message):
    await postgres_db.empty_cart(message.chat.id)
    await message.answer('Корзина пуста')

@rate_limit(limit=5, key = '✅ Корзина')
#@dp.message_handler(text='✅ Корзина')
async def cart(message: types.Message):
    for ret in await postgres_db.sql_read_restaurant_for_availability():
        prov_availability = f'{ret[6]}'
        mess_availability = f'{ret [7]}'
    if str(prov_availability) == '1':
        data = await postgres_db.get_cart(message.chat.id)
        new_data = []
        a = []
        for i in range(len(data)):
            new_data.append(await postgres_db.get_user_product(data[i][2]))
        new_data = [new_data[i][0] for i in range(len(new_data))]
        a = f'Корзина:\n'
        s = 0
        for i in range(len(data)):
            a += f'\n{new_data[i][3]} \nКоличество: {data[i][3]}\nЦена: {new_data[i][5]} x {data[i][3]} = {new_data[i][5]  * data[i][3]}\n'
            s += new_data[i][5]  * data[i][3]
        a += f'\nИтого: {s} рублей'
        data = await postgres_db.get_myself(message.chat.id)
        for ret in data:
            a +=f'\nВаши данные:\n\nИмя: {ret[2]}\nНомер телефона: {ret[3]}\nАдрес: {ret[4]}\nКомментарий к заказу: {ret[5]}'
        await bot.send_message(message.chat.id, a, reply_markup=client_kb.kb_client4)
    else:
        await message.answer(mess_availability)

'''****************************************Ввести количество персон, начало оформления заказа**************************************************'''
@rate_limit(limit=5, key = ('Ввести другое количество персон', 'Оформить заказ'))
@dp.message_handler(text = 'Ввести другое количество персон', state=None)
@dp.message_handler(text = 'Оформить заказ', state=None)
async def order_start(message: types.Message):
    for ret in await postgres_db.sql_read_restaurant_for_availability():
        prov_availability = f'{ret[6]}'
        mess_availability = f'{ret [7]}'
    if str(prov_availability) == '1':
        data = await postgres_db.get_cart(message.chat.id)
        proverka = 0
        for heru in data:
            proverka += heru[2]
        if proverka == 0 or proverka == '' or proverka == 'None':
            await bot.send_message(message.chat.id, f'Пожалуйста, добавьте товар в корзину, перед отправлением заказа!')
        else:
            await FSMclient.tools_c.set()
            await message.reply('Введите количество персон')
    else:
        await message.answer(mess_availability)

@dp.message_handler(state=FSMclient.tools_c)
async def order_start_tools(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tools_c'] = message.text
    tools_c = message.text
    await postgres_db.sql_add_tools_c(tools_c, message.chat.id)
    await state.finish()
    await message.reply('Сохранено')
    await bot.send_message(message.from_user.id, 'Укажите время обработки заказа:', reply_markup=client_kb.kb_client_time_order)

'''****************************************Время обработки заказа**************************************************'''

@rate_limit(limit=5, key = ('Ввести другое время обработки заказа', 'Ко времени'))
@dp.message_handler(text = 'Ввести другое время обработки заказа', state=None)
@dp.message_handler(text = 'Ко времени', state=None)
async def order_start(message: types.Message):
    await FSMclient.time_order_c.set()
    await message.reply('Укажите к какому времени')

@dp.message_handler(state=FSMclient.time_order_c)
async def order_start_tools(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time_order_c'] = message.text
    time_order_c = message.text
    await postgres_db.sql_add_time_order(time_order_c, message.chat.id)
    await state.finish()
    await message.reply('Сохранено')
    await bot.send_message(message.from_user.id, 'Выберете способ получения', reply_markup=client_kb.kb_client_obtaining)

@rate_limit(limit=5, key = 'Как можно скорее')
@dp.message_handler(text = 'Как можно скорее')
async def order_start(message: types.Message):
    time_order = 'Как можно скорее'
    await postgres_db.sql_add_time_order(time_order, message.chat.id)
    await bot.send_message(message.from_user.id, 'Выберете способ получения', reply_markup=client_kb.kb_client_obtaining)

'''****************************************Способ получения**************************************************'''

@rate_limit(limit=5, key = 'Выбрать другой способ получения')
@dp.message_handler(text = 'Выбрать другой способ получения')
async def order_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберете способ получения', reply_markup=client_kb.kb_client_obtaining)

@rate_limit(limit=5, key = 'Доставка курьером')
@dp.message_handler(text = 'Доставка курьером', state=None)
async def order_obtaining_1(message: types.Message):
    await FSMclient.adress_c.set()
    await message.reply('Введите адрес')

@dp.message_handler(state=FSMclient.adress_c)
async def order_obtaining_1_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['adress_c'] = message.text
    adress = message.text
    obtaining = 'Курьером'
    await postgres_db.sql_add_adress_c2(adress, obtaining, message.chat.id)
    await state.finish()
    await message.reply('Сохранено')
    data = await postgres_db.get_cart(message.chat.id)
    new_data = []
    for i in range(len(data)):
        new_data.append(await postgres_db.get_user_product(data[i][2]))
    new_data = [new_data[i][0] for i in range(len(new_data))]
    a = f'Корзина:\n'
    s = 0
    for i in range(len(data)):
        a += f'\n{new_data[i][3]} \nКоличество: {data[i][3]}\nЦена: {new_data[i][5]} x {data[i][3]} = {new_data[i][5] * data[i][3]}\n'
        s += new_data[i][5] * data[i][3]
    limit_price = None
    price_obtaining = None
    gain = 'Курьером'
    for sert in await postgres_db.sql_get_obtaining(message.chat.id):
        obtaining = sert[7]
    for nerf in await postgres_db.sql_get_pickup_obtaining():
        limit_price = nerf[5]
    for kart in await postgres_db.sql_get_pickup_obtaining():
        price_obtaining = kart[4]
    if gain == obtaining:
        if s >= limit_price:
            s += 0
            n = 0
        else:
            s += int(price_obtaining)
            n = int(price_obtaining)
    else:
        s += 0
        n = 0
    a += f'\n\nДоставка: {n} рублей'
    s += n
    a += f'\n\nИтого: {s} рублей'
    data = await postgres_db.get_myself(message.chat.id)
    for ret in data:
        a += f'\nВаши данные:\n\nИмя: {ret[2]}\nНомер телефона: {ret[3]}\nАдрес: {ret[4]}\nКомментарий к заказу: {ret[5]}\nПоложить приборы на количество персон: {ret[6]}\n\nСпособ получения: {ret[7]}\n\nВремя получения: {ret[8]}'
        if f'{ret[3]}' == 'None' or f'{ret[3]}' == '':
            a += f'\n\nВнимание! Номер телефона не указан! Пожалуйста, укажите номер телефона для связи'
    await bot.send_message(message.chat.id, a, reply_markup=client_kb.inkb_client2)
    await message.bot.send_message(message.from_user.id, 'Выберете способ оплаты', reply_markup=client_kb.kb_client_pay)

@rate_limit(limit=5, key = 'Самовывоз')
@dp.message_handler(text = 'Самовывоз')
async def order_obtaining_2(message: types.Message):
    read = await postgres_db.sql_get_pickup_obtaining()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[2], f'\n{ret[3]}')
    data = await postgres_db.get_cart(message.chat.id)
    new_data = []
    for i in range(len(data)):
        new_data.append(await postgres_db.get_user_product(data[i][2]))
    new_data = [new_data[i][0] for i in range(len(new_data))]
    a = f'Корзина:\n'
    s = 0
    for i in range(len(data)):
        a += f'\n{new_data[i][3]} \nКоличество: {data[i][3]}\nЦена: {new_data[i][5]} x {data[i][3]} = {new_data[i][5] * data[i][3]}\n'
        s += new_data[i][5] * data[i][3]
    limit_price = None
    price_obtaining = None
    obtaining = 'Самовывоз'
    await postgres_db.sql_add_obtaining_c2(obtaining, message.chat.id)
    gain = 'Курьером'
    for sert in await postgres_db.sql_get_obtaining(message.chat.id):
        obtaining = sert[7]
    for nerf in await postgres_db.sql_get_pickup_obtaining():
        limit_price = nerf[5]
    for kart in await postgres_db.sql_get_pickup_obtaining():
        price_obtaining = kart[4]
    if gain == obtaining:
        if s >= limit_price:
            s += 0
            n = 0
        else:
            s += int(price_obtaining)
            n = int(price_obtaining)
    else:
        s += 0
        n = 0
    a += f'\n\nДоставка: {n} рублей'
    s += n
    a += f'\n\nИтого: {s} рублей\n'
    data = await postgres_db.get_myself(message.chat.id)
    for ret in data:
        a += f'\nВаши данные:\n\nИмя: {ret[2]}\nНомер телефона: {ret[3]}\nАдрес: {ret[4]}\nКомментарий к заказу: {ret[5]}\nПоложить приборы на количество персон: {ret[6]}\n\nСпособ получения: {ret[7]}\n\nВремя получения: {ret[8]}'
        if f'{ret[3]}' == 'None' or f'{ret[3]}' == '':
            a += f'\n\nВнимание! Номер телефона не указан! Пожалуйста, укажите номер телефона для связи'
    await bot.send_message(message.chat.id, a, reply_markup=client_kb.inkb_client2)
    await message.bot.send_message(message.from_user.id, 'Выберете способ оплаты', reply_markup=client_kb.kb_client_pay)

'''****************************************Выберите способ оплаты**************************************************'''

@rate_limit(limit=5, key = 'Наличными')
@dp.message_handler(text = 'Наличными')
async def pay_nal(message: types.Message):
    await bot.send_message(message.from_user.id, 'Пожалуйста проверьте указанный номер телефона!\n'
                                                 '\nВ случае наличной оплаты, заказ начинают готовить только после устного подтверждения\nНаш менеджер позвонит вам в течение 5 минут',
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Изм номер телефона' , callback_data=f'Изменить номер'),
                     InlineKeyboardButton(text='Отправить заказ', callback_data=f'Отправить заказ')))

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Отправить заказ'))
async def del_send_order(callback_query: types.CallbackQuery):
    data = await postgres_db.get_cart(callback_query.message.chat.id)
    proverka = 0
    for heru in data:
        proverka += heru[2]
    if proverka == 0 or proverka == '' or proverka == 'None':
        await bot.send_message(callback_query.message.chat.id, f'Пожалуйста, добавьте товар в корзину, перед отправлением заказа!')
    else:
        data = await postgres_db.get_cart(callback_query.message.chat.id)
        new_data = []
        for i in range(len(data)):
            new_data.append(await postgres_db.get_user_product(data[i][2]))
        new_data = [new_data[i][0] for i in range(len(new_data))]
        a = f'Корзина:\n'
        s = 0
        for i in range(len(data)):
            a += f'\n{new_data[i][3]} \nКоличество: {data[i][3]}\nЦена: {new_data[i][5]} x {data[i][3]} = {new_data[i][5] * data[i][3]}\n'
            s += new_data[i][5] * data[i][3]
        obtaining = None
        limit_price = None
        price_obtaining = None
        gain = 'Курьером'
        for sert in await postgres_db.sql_get_obtaining(callback_query.message.chat.id):
            obtaining = sert[7]
        for nerf in await postgres_db.sql_get_pickup_obtaining():
            limit_price = nerf[5]
        for kart in await postgres_db.sql_get_pickup_obtaining():
            price_obtaining = kart[4]
        if gain == obtaining:
            if s >= limit_price:
                s += 0
                n = 0
            else:
                s += int(price_obtaining)
                n = int(price_obtaining)
        else:
            s += 0
            n = 0
        a += f'\nДоставка: {n} рублей'
        s += n
        a += f'\n\nИтого: {s} рублей'
        data = await postgres_db.get_myself(callback_query.message.chat.id)
        for ret in data:
            a += f'\n\nВаши данные:\n\nИмя: {ret[2]}\nНомер телефона: {ret[3]}\nАдрес: {ret[4]}\nКомментарий к заказу: {ret[5]}\nПоложить приборы на количество персон: {ret[6]}\n\nСпособ получения: {ret[7]}\n\nВремя получения: {ret[8]}'
        #  получаем время
        tz_russia_asha = pytz.timezone("Asia/Yekaterinburg")
        dt_russia_asha = str( datetime.datetime.now(tz_russia_asha))
        #  генерируем id заказа
        str1 = list('1234567890')
        data_orders_id = 'Список id_order:\n\n'
        for ret in await postgres_db.sql_read_id_orders_user():
            data_orders_id += f'{ret[1]}\n'
        random.shuffle(str1)
        order_id = ''.join([random.choice(str1) for x in range(7)])
        while order_id in data_orders_id:
            random.shuffle(str1)
            order_id = ''.join([random.choice(str1) for x in range(5)])
        #  общий список того что надо передать
        user_id = callback_query.message.chat.id
        id_order = order_id
        cart_order = a
        order_date = dt_russia_asha
        status = 'Не доставлен'
        payment = 'Нал'
        await bot.send_message(callback_query.message.chat.id, a)
        #  добавляем в бд
        await postgres_db.sql_add_order_client_nal(user_id, id_order, cart_order, order_date, status, payment)
        # отправляем сообщение модератору: заказ, его номер, и все данные из корзины и данных клиента на данный момент
        await bot.send_message(Config.admin_ids, f'Заказ {id_order} сформирован, клиент ожидает звонка!\n\n{a}')
        # очищаем корзину
        await postgres_db.empty_cart(callback_query.message.chat.id)
        # отправляем сообщение пользователю: номер заказа, заказ принят, заказ оплачен, ожидайте звонка оператора
        await bot.send_message(callback_query.message.chat.id,
                               f'Заказ {id_order} сохранён и отправлен на рассмотрение, наш менеджер скоро с вами свяжется!')

'''****************************************Оплата**************************************************'''

@rate_limit(limit=5, key = 'Сбербанк')
@dp.message_handler(text='Сбербанк')
async def buy_process(message: types.Message):
    data = await postgres_db.get_cart(message.chat.id)
    proverka = 0
    for heru in data:
        proverka += heru[2]
    if proverka == 0 or proverka == '' or proverka == 'None':
        await bot.send_message(message.chat.id, f'Пожалуйста, добавьте товар в корзину, перед отправлением заказа!')
    else:
        new_data = []
        for i in range(len(data)):
            new_data.append(await postgres_db.get_user_product(data[i][2]))
        new_data = [new_data[i][0] for i in range(len(new_data))]
        s = 0
        for i in range(len(data)):
            s += new_data[i][5] * data[i][3]
        obtaining = None
        limit_price = None
        price_obtaining = None
        gain = 'Курьером'
        for sert in await postgres_db.sql_get_obtaining(message.chat.id):
            obtaining = sert[7]
        for nerf in await postgres_db.sql_get_pickup_obtaining():
            limit_price = nerf[5]
        for kart in await postgres_db.sql_get_pickup_obtaining():
            price_obtaining = kart[4]
        if gain == obtaining:
            if s >= limit_price:
                s += 0
                n = 0
            else:
                s += int(price_obtaining)
                n = int(price_obtaining)
        else:
            n = 0
            s += 0
        s += n
        data = await postgres_db.get_cart(message.chat.id)
        new_data = []
        for i in range(len(data)):
            new_data.append(await postgres_db.get_user_product(data[i][2]))
        new_data = [new_data[i][0] for i in range(len(new_data))]
        prices = [LabeledPrice(label=new_data[i][3]+f' x {data[i][3]}', amount= new_data[i][5] * 100 * data[i][3]) for i in range(len(new_data))]
        prices += [LabeledPrice(label=f'Доставка', amount= n * 100 )]
        await bot.send_invoice(message.chat.id,
                               title='кусочек удовольствия',
                               description='Менеджер позвонит вам на указанный номер телефона - пожалуйста, будьте на связи',
                               provider_token=Config.pay_token,
                               currency='rub',
                               need_email=False,
                               prices=prices,
                               start_parameter='example',
                               payload='some_invoice')

@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def s_pay(message: types.Message):
    data = await postgres_db.get_cart(message.chat.id)
    new_data = []
    a = []
    for i in range(len(data)):
        new_data.append(await postgres_db.get_user_product(data[i][2]))
    new_data = [new_data[i][0] for i in range(len(new_data))]
    a = f'Корзина:\n'
    s = 0
    proverka = ''
    for i in range(len(data)):
        a += f'\n{new_data[i][3]} \nКоличество: {data[i][3]}\nЦена: {new_data[i][5]} x {data[i][3]} = {new_data[i][5] * data[i][3]}\n'
        proverka += str({new_data[i][3]})
        s += new_data[i][5] * data[i][3]
    obtaining = None
    limit_price = None
    price_obtaining = None
    gain = 'Курьером'
    for sert in await postgres_db.sql_get_obtaining(message.chat.id):
        obtaining = sert[7]
    for nerf in await postgres_db.sql_get_pickup_obtaining():
        limit_price = nerf[5]
    for kart in await postgres_db.sql_get_pickup_obtaining():
        price_obtaining = kart[4]
    if gain == obtaining:
        if s >= limit_price:
            s += 0
            n = 0
        else:
            s += int(price_obtaining)
            n = int(price_obtaining)
    else:
        n = 0
        s += 0
    a += f'\nДоставка: {n} рублей'
    s += n
    a += f'\n\nИтого: {s} рублей'
    data = await postgres_db.get_myself(message.chat.id)
    for ret in data:
        a += f'\n\nВаши данные:\n\nИмя: {ret[2]}\nНомер телефона: {ret[3]}\nАдрес: {ret[4]}\nКомментарий к заказу: {ret[5]}\nПоложить приборы на количество персон: {ret[6]}\n\nСпособ получения: {ret[7]}\n\nВремя получения: {ret[8]}'

    #  получаем время
    tz_russia_asha = pytz.timezone("Asia/Yekaterinburg")
    dt_russia_asha = str(datetime.datetime.now(tz_russia_asha))
    # datetime_obj = datetime.strptime(dt_russia_asha, '%m/%d/%y %H:%M:%S')
    # date_obj = datetime.datetime.strptime(dt_russia_asha, '%m/%d/%y')
    #  генерируем id заказа
    str1 = list('1234567890')
    data_orders_id = 'Список id_order:\n\n'
    for ret in await postgres_db.sql_read_id_orders_user():
        data_orders_id += f'{ret[1]}\n'
    random.shuffle(str1)
    order_id = ''.join([random.choice(str1) for x in range(7)])
    while order_id in data_orders_id:
        random.shuffle(str1)
        order_id = ''.join([random.choice(str1) for x in range(5)])
    #  общий список того что надо передать
    user_id = message.chat.id
    id_order = order_id
    cart_order = a
    order_date = dt_russia_asha
    status = 'Не доставлен'
    payment = 'Безнал'

    if proverka == 0 or proverka == 'None':
        await bot.send_message(message.chat.id, f'Пожалуйста, добавьте товар в корзину, перед отправлением заказа!')
    else:
        #  добавляем в бд
        await postgres_db.sql_add_order_client_nal(user_id, id_order, cart_order, order_date, status, payment)
        # отправляем сообщение модератору: заказ, его номер, и все данные из корзины и данных клиента на данный момент
        await bot.send_message(Config.admin_ids, f'Заказ {id_order} сформирован, клиент ожидает звонка!\n\n{a}')
        # очищаем корзину
        await postgres_db.empty_cart(message.chat.id)
        # отправляем сообщение пользователю: номер заказа, заказ принят, заказ оплачен, ожидайте звонка оператора
        await bot.send_message(message.chat.id, f'Платеж прошел успешно!!!\n\nЗаказ {id_order} сохранён и отправлен на рассмотрение, наш менеджер скоро с вами свяжется!')

'''****************************************Возврат к главному меню**************************************************'''
@rate_limit(limit=5, key = 'Главное меню')
@dp.message_handler(text = 'Главное меню')
async def commands_back(message: types.Message):
    await message.bot.send_message(message.from_user.id, 'Переход в главное меню', reply_markup=client_kb.kb_client)

'''******************************************Акции и скидки***********************************************'''

@rate_limit(limit=5, key = '🎁 Акции и скидки')
#@dp.message_handler(text='🎁 Акции и скидки')
async def commands_news(message: types.Message):
    await postgres_db.sql_read_promotion(message)

'''***************** Логика кнопки "отмена", для прерывания любого процесса *************************'''

# Выход из состояний
@dp.message_handler(state='*', commands=['отмена'])
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ок')

'''*********************************************** Мои данные *******************************************************'''
@rate_limit(limit=5, key = ('Изменить мои данные', '💚 Мои данные'))
@dp.message_handler(text = 'Изменить мои данные')
@dp.message_handler(text = '💚 Мои данные')
async def commands_myself(message: types.Message):
    data = await postgres_db.get_myself(message.chat.id)
    for ret in data:
        await bot.send_message(message.from_user.id, f'Ваши данные:\nИмя: {ret[2]}\nНомер телефона: {ret[3]}\nАдрес: {ret[4]}\nКомментарий к заказу: {ret[5]}', reply_markup=client_kb.inkb_client2)

#Начало диалога Изменить_имя
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Изменить имя'), state=None)
async def change_name_c(CallbackQuery: types.CallbackQuery):
    await FSMclient.name_c.set()
    await CallbackQuery.answer(text=f'Введите имя или "Отмена"', show_alert = True)
    # await CallbackQuery.answer('Введите имя или "Отмена" ')

# Ловим ответ на Изменить_имя
@dp.message_handler(state=FSMclient.name_c)
async def change_name_c2 (message: types.Message, state: FSMContext):
    name_c = message.text
    await postgres_db.sql_add_name_c(name_c, message.chat.id)
    await state.finish()
    await message.reply('Имя изменено!')

#Начало диалога Изменить_номер
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Изменить номер'), state=None)
async def change_number_c(CallbackQuery: types.CallbackQuery):
    await FSMclient.number_c.set()
    await CallbackQuery.answer(text=f'Введите номер или "Отмена"', show_alert=True)
    # await CallbackQuery.answer('Введите номер или "Отмена" ')

# Ловим ответ на Изменить_номер
@dp.message_handler(state=FSMclient.number_c)
async def change_number_c2 (message: types.Message, state: FSMContext):
    number_c = message.text
    await postgres_db.sql_add_number_c(number_c, message.chat.id)
    await state.finish()
    await message.reply('Номер изменён!')

#Начало диалога Изменить_адрес
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Изменить адрес'), state=None)
async def change_adress_c(CallbackQuery: types.CallbackQuery):
    await FSMclient.adress_c_1.set()
    await CallbackQuery.answer(text=f'Введите адрес или "Отмена"', show_alert=True)
    # await CallbackQuery.answer('Введите адрес или "Отмена" ')

# Ловим ответ на Изменить_адрес
@dp.message_handler(state=FSMclient.adress_c_1)
async def change_adress_c2 (message: types.Message, state: FSMContext):
    adress_c_1 = message.text
    await postgres_db.sql_add_adress_c(adress_c_1, message.chat.id)
    await state.finish()
    await message.reply('Адрес изменён!')

#Начало диалога Изменить_комментарий к заказу
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Изменить комментарий к заказу'), state=None)
async def change_commentary_c(CallbackQuery: types.CallbackQuery):
    await FSMclient.commentary_c.set()
    await CallbackQuery.answer(text=f'Введите комментарий к заказу или "Отмена"', show_alert=True)
    # await CallbackQuery.answer('Введите комментарий к заказу или "Отмена" ')

# Ловим ответ на Изменить_комментарий к заказу
@dp.message_handler(state=FSMclient.commentary_c)
async def change_commentary_c2 (message: types.Message, state: FSMContext):
    commentary_c = message.text
    await postgres_db.sql_add_commentary_c(commentary_c, message.chat.id)
    await state.finish()
    await message.reply('Комментарий к заказу изменён!')

'''*********************************************** Регистрация хэндлеров *******************************************************'''

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start'])
    dp.register_message_handler(commands_location, text='👨‍🍳 Информация о заведении')
    dp.register_message_handler(commands_products, text='🍰 Меню')
    dp.register_message_handler(commands_news, text='🎁 Акции и скидки')
    dp.register_message_handler(commands_myself, text='💚 Мои данные')
    dp.register_message_handler(cart, text='✅ Корзина')
