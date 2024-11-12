

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from database import sqlrequests
from keyboards import admin_kb, client_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime, random, pytz

from config import Config
ID = Config.admin_id

#создаём класс наследующий Statesgroup, запускаем атрибуты state для FSMашины
class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    restaurant_f = State()
    photo_promotion = State()
    name_promotion = State()
    description_promotion = State()
    photo_anonce = State()
    description_anonce = State()
    categories_name = State()
    pos_cat = State()
    product_id_add = State()
    photo_restaurant_pickup = State()
    description_restaurant = State()
    restaurant_price_obtain = State()
    restaurant_limit_price = State()
    availability = State()
    availability_cat = State()
    order_client_id = State()
    comment_order_client_id = State()
    order_client_id_n = State()
    order_client_id_nl = State()
    restaurant_availability = State()
    phone_client_order = State()

#Получаем ID текущего модератора
#@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Режим модератора активирован', reply_markup=admin_kb.button_case_admin)

'''***************** Логика кнопок "Изменить_позицию_меню" *************************'''

#Начало диалога загрузки нового пункта меню
#Начало диалога Изменить_категории
@dp.message_handler(commands=['Изменить_позицию_меню'])
async def change_pos_menu(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.chat.id, 'Переходим к изменению позиции меню', reply_markup=admin_kb.kb_admin_pos)

@dp.message_handler(commands=['Добавить_позицию_меню'], state=None)
async def change_pos_menu2(message: types.Message):
    if message.from_user.id == ID:
        try:
            msg_for_name_categories = 'Список категорий:\n'
            data = await sqlrequests.get_categories_name()
            for i in data:
                msg_for_name_categories += f'\n{i}'
            msg_for_name_categories += '\n\nВведи название категории, к которой будет добавлена позиция: \n(Без лишних символов, типо пробела, только так, как записана категория выше)\nили "Отмена"'
            await message.answer(msg_for_name_categories)
        except:
            msg_for_name_categories = '\n\nВведи название категории, к которой будет добавлена позиция: \n(Без лишних символов, типо пробела, только так, как записана категория выше)\nили "Отмена"'
            await message.answer(msg_for_name_categories)
        await FSMadmin.pos_cat.set()

@dp.message_handler(state=FSMadmin.pos_cat)
async def hange_categories_add_end(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        name_cat = message.text
        data_cat_name = 'Список категорий:\n\n'
        for ret in await sqlrequests.get_categories_name():
            data_cat_name += f'{ret.category_name}\n'
        data_cat_dict = {}
        for s in await sqlrequests.get_all_categories():
            # data_cat_dict[s[0]] = s[1]
            data_cat_dict[s.category_name] = s.category_id
        if name_cat in data_cat_name:
            key = name_cat
            number_cat_pos = data_cat_dict[key]
            str1 = list('123456789')
            data_products_id = 'Список product_id:\n\n'
            for ret in await sqlrequests.sql_read2_products():
                data_products_id += f'{ret[1]}\n'
            random.shuffle(str1)
            product_id = ''.join([random.choice(str1) for x in range(5)])
            while product_id in data_products_id:
                random.shuffle(str1)
                product_id = ''.join([random.choice(str1) for x in range(5)])
            async with state.proxy() as data:
                data['product_id'] = product_id
            async with state.proxy() as data:
                data['category_id'] = number_cat_pos
            await message.reply('Теперь загрузи фото')
            await FSMadmin.photo.set()
        else:
            data_cat_name += f'\n\nВведённой категории нет в базе данных, ознакомься со списком и начни добавление позиции заново'
            await bot.send_message(message.chat.id, data_cat_name)
            await state.finish()

'''***************** Логика кнопки "отмена", для прерывания любого процесса *************************'''

# Выход из состояний
#@dp.message_handler(state='*', commands=['отмена'])
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Ок')

'''***************** Продолжение логики кнопок "Загрузить_позицию_каталога", "Удалить_позицию_каталога" *************************'''

#@dp.message_handler(content_types=['photo'], state=FSMadmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['img'] = message.photo[2].file_id
        await FSMadmin.next()
        await message.reply('Теперь введи название или "Отмена"')

# Ловим второй ответ
#@dp.message_handler(state=FSMadmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMadmin.next()
        await message.reply('Введи описание или "Отмена"')

# Ловим третий ответ
#@dp.message_handler(state=FSMadmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMadmin.next()
        await message.reply('Теперь укажи цену или "Отмена"')

# Ловим последний ответ и используем поулченные данные
#@dp.message_handler(state=FSMadmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
            data['availability'] = 1
        await sqlrequests.sql_add_command_products(state)
        await state.finish()
        await message.reply('Добавление позиции завершено')

@dp.message_handler(commands=['Стоп_Вкл_позиция'])
async def change_pos_menu(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.chat.id, 'Переходим к стоп листу позиций')
        read = await sqlrequests.get_all_products()
        for ret in read:
            if f'{ret[7]}'==str(1):
                availability = 'Включен'
            else:
                availability = 'Выключен'
            await bot.send_message(message.from_user.id,f'{ret[3]}\nДоступность: {availability}\n', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'Включить {ret[3]}', callback_data=f'Включить позицию {ret[1]}'),
                InlineKeyboardButton(f'Выключить {ret[3]}', callback_data=f'Выключить позицию {ret[1]}')))

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Включить позицию '))
async def callback_turn_on_products(callback_query: types.CallbackQuery):
    await sqlrequests.sql_turn_on_products(callback_query.data.replace('Включить позицию ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("Включить позицию ", "")} включена.', show_alert=True)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Выключить позицию '))
async def callback_turn_off_products(callback_query: types.CallbackQuery):
    await sqlrequests.sql_turn_off_products(callback_query.data.replace('Выключить позицию ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("Выключить позицию ", "")} выключена.', show_alert=True)

'''*********************************************************'''

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del_pos'))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlrequests.sql_delete_command_products(callback_query.data.replace('del_pos', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del", "")} удалена.', show_alert=True)

@dp.message_handler(commands=['Удалить_позицию_меню'])
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlrequests.sql_read2_products()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[2], f'{ret[3]}\nОписание: {ret[4]}\nЦена {ret[5]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {ret[3]}', callback_data=f'del_pos {ret[0]}')))

'''***************** Логика кнопок "Изменить_категории" *****************'''

#Начало диалога Изменить_категории
@dp.message_handler(commands=['Изменить_категории'])
async def change_categories(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.chat.id, 'Переходим к изменению категории', reply_markup=admin_kb.kb_admin_cat)

@dp.message_handler(commands=['Меню_модератора'])
async def change_categories(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.chat.id, 'Переходим к меню модератора', reply_markup=admin_kb.button_case_admin)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del_cat '))
async def del_callback_cat_del(callback_query: types.CallbackQuery):
    await sqlrequests.sql_delete_category(callback_query.data.replace('del_cat ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del_cat ", "")} удален.', show_alert=True)

@dp.message_handler(commands=['Удалить_категорию'])
async def change_categories_del(message: types.Message):
    if message.from_user.id == ID:
        data = await sqlrequests.get_categories_name()
        for i in data:
            await bot.send_message(message.from_user.id, i[0])
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {i[0]}', callback_data=f'del_cat {i[0]}')))

@dp.message_handler(commands=['Стоп_Вкл_категория'])
async def change_cat_menu(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.chat.id, 'Переходим к стоп листу позиций')
        read = await sqlrequests.get_all_categories()
        for ret in read:
            if f'{ret[2]}' == str(1):
                availability_cat = f'Включен'
            else:
                availability_cat = f'Выключен'
            await bot.send_message(message.from_user.id,f'{ret[0]}\nДоступность: {availability_cat}\n')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Включить {ret[0]}', callback_data=f'Включить категорию {ret[1]}'),
                                                                                                             InlineKeyboardButton(f'Выключить {ret[0]}', callback_data=f'Выключить категорию {ret[1]}')))
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Включить категорию '))
async def callback_turn_on_category(callback_query: types.CallbackQuery):
    await sqlrequests.sql_turn_on_category(callback_query.data.replace('Включить категорию ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("Включить категорию ", "")} включена.', show_alert=True)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Выключить категорию '))
async def callback_turn_off_category(callback_query: types.CallbackQuery):
    await sqlrequests.sql_turn_off_category(callback_query.data.replace('Выключить категорию ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("Выключить категорию ", "")} выключена.', show_alert=True)

@dp.message_handler(commands=['Добавить_категорию'], state=None)
async def change_categories_add(message: types.Message):
    if message.from_user.id == ID:
        try:
            msg_for_name_categories = 'Список категорий:\n\n'
            for i in await sqlrequests.get_categories_name():
                msg_for_name_categories += f'{i[0]}\n'
            msg_for_name_categories += '\nВведи название :\n(Без лишних символов, типо пробела на конце)\nили "Отмена"'
            await message.answer(msg_for_name_categories)
        except:
            msg_for_name_categories = '\nВведи название :\n(Без лишних символов, типо пробела на конце)\nили "Отмена"'
            await message.answer(msg_for_name_categories)
        await FSMadmin.categories_name.set()

@dp.message_handler(state=FSMadmin.categories_name)
async def hange_categories_add_end (message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['category_name'] = message.text
            data['availability_cat'] = 1
        await sqlrequests.sql_add_categories(state)
        await state.finish()
        await message.reply('Новая категория внесена')

'''***************** Логика кнопок "Работа_с_заказами"***************** '''

@dp.message_handler(commands=['Работа_с_заказами'])
async def change_categories(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.chat.id, 'Переходим к работе с заказами', reply_markup=admin_kb.kb_admin_orders)

@dp.message_handler(commands=['Подтвердить_доставку_заказа'], state=None)
async def confirm_delivery(message: types.Message):
    if message.from_user.id == ID:
        data_orders_client_id_n = ''
        for ret in await sqlrequests.sql_read_id_orders_user_not_deliv():
            data_orders_client_id_n += f'{ret[1]}\n'
        msg_for_name_categories = f'На данный момент есть следующие заказы, ожидающие подтверждения:\n{data_orders_client_id_n}\n\nВведи id заказа или "Отмена": \n(Без лишних символов, типо пробела)'
        await message.answer(msg_for_name_categories)
        await FSMadmin.order_client_id.set()

@dp.message_handler(state=FSMadmin.order_client_id)
async def confirm_delivery_end(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        order_client_id_1 = message.text
        data_orders_client_id = 'Список id заказов:\n\n'
        for ret in await sqlrequests.sql_read_id_orders_user():
            data_orders_client_id += f'{ret[1]}\n'
        if order_client_id_1 in data_orders_client_id:
            tz_russia_asha = pytz.timezone("Asia/Yekaterinburg")
            dt_russia_asha = str(datetime.datetime.now(tz_russia_asha))
            receiving = dt_russia_asha
            await sqlrequests.sql_update_status_orders_user(order_client_id_1, receiving)
            await message.reply('Доставка заказ подтверждена')
            id_client= ''
            for ret in await sqlrequests.sql_get_user_id_orders_client(order_client_id_1):
                id_client = f'{ret[2]}'
            await bot.send_message(id_client, f'Приятного аппетита! Как вам заказ?\nМожете написать свой отзыв в нашей группе ВК! (ссылка)')
            await state.finish()
        else:
            data_cat_name = f'\n\nВведённого id заказа нет в базе данных, начни подтверждение доставки заново'
            await bot.send_message(message.chat.id, data_cat_name)
            await state.finish()

@dp.message_handler(commands=['Комментарий_к_заказу'], state=None)
async def comment_order(message: types.Message):
    msg_for_name_categories = '\n\nВведи id заказа или "Отмена": \n(Без лишних символов, типо пробела)'
    await message.answer(msg_for_name_categories)
    await FSMadmin.order_client_id_n.set()

@dp.message_handler(state=FSMadmin.order_client_id_n)
async def comment_order2(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        order_client_id_1 = message.text
        data_orders_client_id = 'Список id заказов:\n\n'
        for ret in await sqlrequests.sql_read_id_orders_user():
            data_orders_client_id += f'{ret[1]}\n'
        if order_client_id_1 in data_orders_client_id:
            async with state.proxy() as data:
                data['order_client_id_n'] = message.text
            await message.reply('Введи комментарий или "Отмена"')
            await FSMadmin.comment_order_client_id.set()
        else:
            data_cat_name = f'\n\nВведённого id заказа нет в базе данных, начни подтверждение доставки заново'
            await bot.send_message(message.chat.id, data_cat_name)

@dp.message_handler(state=FSMadmin.comment_order_client_id)
async def comment_order3(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['comment_order_client_id'] = message.text
        id_order = data['order_client_id_n']
        commentary = data['comment_order_client_id']
        await sqlrequests.sql_update_comment_orders_user(id_order, commentary)
        await message.reply('Комментарий добавлен')
        await state.finish()

@dp.message_handler(commands=['Заказы_клиента'], state=None)
async def client_orders_viewing(message: types.Message):
    if message.from_user.id == ID:
        msg_for_name_categories = '\n\nВведи номер телефона клиента или "Отмена": \n(Без лишних символов, типо пробела)'
        await message.answer(msg_for_name_categories)
        await FSMadmin.phone_client_order.set()

@dp.message_handler(state=FSMadmin.phone_client_order)
async def client_orders_viewing2(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        cl_phone = message.text
        data_cl_numbers = 'Список номеров:\n\n'
        for ret in await sqlrequests.sql_read_phone_numbers_user():
            data_cl_numbers += f'{ret[3]}\n'
        data_cat_dict = {}
        for s in await sqlrequests.sql_read_phone_numbers_user():
            data_cat_dict[s[3]] = s[1]
        if cl_phone in data_cl_numbers:
            key = cl_phone
            id_clients = data_cat_dict[key]
            data_products_id = f'ID клиента {id_clients}\n\nСписок заказов:\n\n'
            for ret in await sqlrequests.sql_get_user_id_orders(id_clients):
                data_products_id += f'id заказа: {ret[1]}\nСтатус заказа: {ret[6]}\nДата заказа: {ret[4]}\nОплата: {ret[7]}\nКомментарий от модератора: {ret[8]}\n\n'
            await bot.send_message(message.chat.id, data_products_id)
            await message.reply('Выгрузка заказов окончена')
            await state.finish()
        else:
            data_cat_name = f'\n\nВведённого номера телефона нет в базе данных, начни поиск заказов клиента заново'
            await bot.send_message(message.chat.id, data_cat_name)
            await state.finish()

@dp.message_handler(commands=['Посмотреть_заказ'], state=None)
async def look_order(message: types.Message):
    msg_for_name_categories = '\n\nВведи id заказа или "Отмена": \n(Без лишних символов, типо пробела)'
    await message.answer(msg_for_name_categories)
    await FSMadmin.order_client_id_nl.set()

@dp.message_handler(state=FSMadmin.order_client_id_nl)
async def look_order2(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        order_client_id_1 = message.text
        data_orders_client_id = 'Список id заказов:\n\n'
        for ret in await sqlrequests.sql_read_id_orders_user():
            data_orders_client_id += f'{ret[1]}\n'
        if order_client_id_1 in data_orders_client_id:
            for ret in await sqlrequests.sql_get_user_id_orders_client(order_client_id_1):
                data_products_id = f'id клиента: {ret[2]}\nid заказа: {ret[1]}\n\nКорзина клиента:\n\n {ret[3]}\n\nДата и время создания заказа: {ret[4]}\nДата и время получения заказа: {ret[5]}\nСтатус заказа: {ret[6]}\nОплата: {ret[7]}\nКомментарий от модератора: {ret[8]}\n\n\n'
            await bot.send_message(message.chat.id, data_products_id)
            await message.reply('Выгрузка заказа окончена')
            await state.finish()
        else:
            data_cat_name = f'\n\nВведённого id заказа нет в базе данных, начни поиск заново'
            await bot.send_message(message.chat.id, data_cat_name)
            await state.finish()

'''***************** Логика кнопок "Акция/скидка***************** "'''

#Начало диалога Сделать_объявление
@dp.message_handler(commands='Акция/скидка')
async def start_promotion_kb(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.chat.id, 'Переходим к редактированию акции/скидок', reply_markup=admin_kb.kb_admin_promotion)

#Начало диалога загрузки нового пункта меню
#@dp.message_handler(commands='Новая_акция/скидка', state=None)
async def start_promotion(message: types.Message):
    if message.from_user.id == ID:
        await FSMadmin.photo_promotion.set()
        await message.reply('Загрузи фото')

# Ловим первый ответ и пишем в словарь
#@dp.message_handler(content_types=['photo'], state=FSMadmin.photo_promotion)
async def load_photo_promotion(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo_promotion'] = message.photo[0].file_id
        await FSMadmin.next()
        await message.reply('Теперь введи название')

# Ловим второй ответ
#@dp.message_handler(state=FSMadmin.name_promotion)
async def load_name_promotion(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name_promotion'] = message.text
        await FSMadmin.next()
        await message.reply('Введи описание')

# Ловим третий ответ
#@dp.message_handler(state=FSMadmin.description_promotion)
async def load_description_promotion(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description_promotion'] = message.text
        await sqlrequests.sql_add_command_promotion(state)
        await state.finish()
        await message.reply('Информация об акциях и скидках обновлена')

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('fel '))
async def del_callback_run_promotion(callback_query: types.CallbackQuery):
    await sqlrequests.sql_delete_command_promotion(callback_query.data.replace('fel ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("fel ", "")} удалена.', show_alert=True)

@dp.message_handler(commands=['Удалить_акцию_скидку'])
async def delete_item_promotion(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlrequests.sql_read2_promotion()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'fel {ret[1]}')))

'''***************** Логика кнопки "Стоп_заказы" *************************'''

@dp.message_handler(commands='Стоп_заказы')
async def stop_orders(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.chat.id, 'Переходим к редактированию активности заведения', reply_markup=admin_kb.kb_admin_availability)

@dp.message_handler(commands='Выключить_заказы')
async def stop_orders(message: types.Message):
    if message.from_user.id == ID:
        await sqlrequests.sql_stop_orders()
        await bot.send_message(message.chat.id, 'Заведение выключено и теперь будет отвечать сообщением, которое вы можете изменить "Сообщение_для_пользователя"')

@dp.message_handler(commands='Включить_заказы')
async def stop_orders(message: types.Message):
    if message.from_user.id == ID:
        await sqlrequests.sql_start_orders()
        await bot.send_message(message.chat.id, 'Заведение включено и работает в стандартном режиме')

@dp.message_handler(commands='Сообщение_для_пользователя', state=None)
async def start_restaurant_mess(message: types.Message):
    if message.from_user.id == ID:
        for ret in await sqlrequests.sql_read_restaurant_for_availability():
            mess_availability = f'{ret[7]}'
        await bot.send_message(message.chat.id, f'На данный момент сообщение для пользователя следующее:\n\n{mess_availability}')
        await FSMadmin.restaurant_availability.set()
        await message.reply('Введи сообщение, которое получит пользователь при остановке заведения!')

@dp.message_handler(state=FSMadmin.restaurant_availability)
async def end_restaurant_mess (message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['restaurant_availability'] = message.text
        durostb = message.text
        await sqlrequests.sql_add_mess_for_availability(durostb)
        await state.finish()
        await message.reply('Сообщение для пользователя изменено!')

'''***************** Логика кнопки "Изменить_информацию_о_заведении" *************************'''

@dp.message_handler(commands = 'Изменить_данные_ресторана')
async def start_restaurant_base(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, 'Выбери раздел', reply_markup=admin_kb.kb_admin_restaurant)

#Начало диалога Изменить_информацию_о_заведении
#@dp.message_handler(commands='Изменить_информацию_о_заведении', state=None)
async def start_restaurant(message: types.Message):
    if message.from_user.id == ID:
        await FSMadmin.restaurant_f.set()
        await message.reply('Напиши расположение заведения, время работы, среднее время доставки, время работы и т.д.\nили напиши "Отмена"')

# Ловим ответ на Изменить_информацию_о_заведении
#@dp.message_handler(state=FSMadmin.restaurant_f)
async def end_restaurant (message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['restaurant_f'] = message.text
        location_time = message.text
        await sqlrequests.sql_add_restaurant(location_time)
        await state.finish()
        await message.reply('Информация о заведении изменена')

#Начало диалога Изменить_информацию_о_самовывозе
@dp.message_handler(commands='Изменить_информацию_о_самовывозе', state=None)
async def start_restaurant_pickup(message: types.Message):
    if message.from_user.id == ID:
        await FSMadmin.photo_restaurant_pickup.set()
        await message.reply('Загрузи фото расположения самовывоза\nили напиши "Отмена"')

# Ловим первый ответ и пишем в словарь
@dp.message_handler(content_types=['photo'], state=FSMadmin.photo_restaurant_pickup)
async def load_photo_restaurant(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo_restaurant_pickup'] = message.photo[0].file_id
        await FSMadmin.next()
        await message.reply('Теперь введи описание\nили напиши "Отмена"')

# Ловим второй ответ
@dp.message_handler(state=FSMadmin.description_restaurant)
async def load_description_restaurant(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description_restaurant'] = message.text
        photo_restaurant_pickup = data['photo_restaurant_pickup']
        description_restaurant = data['description_restaurant']
        await sqlrequests.sql_add_restaurant_pickup(photo_restaurant_pickup, description_restaurant)
        await state.finish()
        await message.reply('Информация о самовывозе изменена')

#Начало диалога Изменить_цену_доставки
@dp.message_handler(commands='Изменить_цену_доставки', state=None)
async def start_restaurant_price_obtain(message: types.Message):
    if message.from_user.id == ID:
        await FSMadmin.restaurant_price_obtain.set()
        await message.reply('Напиши цену доставки\nили напиши "Отмена"')

# Ловим ответ на Изменить_цену_доставки
@dp.message_handler(state=FSMadmin.restaurant_price_obtain)
async def end_restaurant_price_obtain (message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['restaurant_price_obtain'] = message.text
        restaurant_price_obtain = data['restaurant_price_obtain']
        await sqlrequests.sql_add_restaurant_price_obtain(restaurant_price_obtain)
        await state.finish()
        await message.reply('Информация о цене доставки изменена')

#Начало диалога Изменить_предел_цены_бесплатной_доставки
@dp.message_handler(commands='Изменить_предел_цены_бесплатной_доставки', state=None)
async def start_restaurant_limit_price(message: types.Message):
    if message.from_user.id == ID:
        await FSMadmin.restaurant_limit_price.set()
        await message.reply('Напиши предел цены бесплатной доставки\nили напиши "Отмена"')

# Ловим ответ на Изменить_предел_цены_бесплатной_доставки
@dp.message_handler(state=FSMadmin.restaurant_limit_price)
async def end_restaurant_limit_price (message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['restaurant_limit_price'] = message.text
        restaurant_limit_price = data['restaurant_limit_price']
        await sqlrequests.sql_add_restaurant_limit_price(restaurant_limit_price)
        await state.finish()
        await message.reply('Информация о пределе цены бесплатной доставки изменена')

'''***************** Логика кнопки "Сделать_объявление" *************************'''

#Начало диалога Сделать_объявление
@dp.message_handler(commands='Сделать_объявление')
async def start_anonce(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.chat.id, 'Переходим к объявлению', reply_markup=admin_kb.kb_admin_anounce)

#Начало диалога Создать_объявление
@dp.message_handler(commands='Создать_объявление', state=None)
async def start_anonce_add(message: types.Message):
    if message.from_user.id == ID:
        await FSMadmin.photo_anonce.set()
        await message.reply('Загрузи фото')

#@dp.message_handler(content_types=['photo'], state=FSMadmin.photo_anonce)
async def load_photo_anonce(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo_anonce'] = message.photo[0].file_id
        await FSMadmin.next()
        await message.reply('Теперь введи описание')

#@dp.message_handler(state=FSMadmin.description_anonce)
async def load_description_anonce(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description_anonce'] = message.text
        await sqlrequests.sql_add_command_anonce(state)
        await state.finish()
        await message.reply('Информация обновлена')

#Начало диалога Объявить_или_удалить_новость
@dp.message_handler(commands='Объявить_или_удалить_объявление')
async def start_anonce_or_del(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlrequests.sql_read2_anonce()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(text='Объявить_новость', callback_data=f'sel {ret[1]}')).add(
                InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'tel {ret[1]}')))

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('sel '))
async def anonce_handler(message: types.Message):
    if message.from_user.id == ID:
        sam = await sqlrequests.sql_read2_anonce()
        data_users = []
        for s in await sqlrequests.sql_read3_users():
            data_users.append(s)
        for row in data_users:
            try:
                for ret in sam:
                    await bot.send_photo(row[0], ret[0], f'{ret[1]}')
                    await bot.send_message(message.from_user.id, f'Рассылка прошла успешно, пользователю {row[0]}')
            except:
                pass

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('tel '))
async def del_callback_run_anonce(callback_query: types.CallbackQuery):
    await sqlrequests.sql_delete_command_anonce(callback_query.data.replace('tel ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("tel ", "")} удалена.', show_alert=True)

'''********************Кнопка перевода на клиентскую менюшку********************************'''

#@dp.message_handler(commands='Режим_пользователя')
async def in_user(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, 'Переходим в главное меню', reply_markup=client_kb.kb_client)

'''******************** Регистрируем хэндлеры ********************************'''

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, state='*', commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMadmin.photo)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_description, state=FSMadmin.description)
    dp.register_message_handler(load_price, state=FSMadmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(in_user, commands=['Режим_пользователя'])
    dp.register_message_handler(start_restaurant, commands=['Изменить_информацию_о_заведении'], state=None)
    dp.register_message_handler(end_restaurant, state=FSMadmin.restaurant_f)
    dp.register_message_handler(start_promotion, commands=['Новая_акция/скидка'], state=None)
    dp.register_message_handler(load_photo_promotion, content_types=['photo'], state=FSMadmin.photo_promotion)
    dp.register_message_handler(load_name_promotion, state=FSMadmin.name_promotion)
    dp.register_message_handler(load_description_promotion, state=FSMadmin.description_promotion)
    dp.register_message_handler(start_anonce_add, commands=['Создать_объявление'], state='*')
    dp.register_message_handler(load_photo_anonce, content_types=['photo'], state=FSMadmin.photo_anonce)
    dp.register_message_handler(load_description_anonce, state=FSMadmin.description_anonce)

