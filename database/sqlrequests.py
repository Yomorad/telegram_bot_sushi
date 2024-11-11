
# import sqlite3 as sq
import psycopg2 as sq

from create_bot import bot
from config import Config
# создаём если нет таблицы с нужными параметрами, кидаем оповещение в консоли
def sql_start():
    global base, cur
    base = sq.connect(database = Config.name_db, user = Config.user_db, host = Config.host_db, password = Config.password_db)
    cur = base.cursor()
    if base:
        print('Data base connected OK')
    cur.execute('CREATE TABLE IF NOT EXISTS products(id SERIAL PRIMARY KEY, product_id INTEGER UNIQUE, img TEXT, name TEXT, description TEXT, price INT, category_id INT, availability INTEGER)')
    cur.execute("CREATE TABLE IF NOT EXISTS restaurant(id SERIAL PRIMARY KEY, location_time TEXT, img TEXT, description TEXT, price_obtain INTEGER, limit_price INTEGER, availability INTEGER, availability_mess TEXT)")
    cur.execute('CREATE TABLE IF NOT EXISTS promotion(img TEXT, name SERIAL PRIMARY KEY, description TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS anonce(img TEXT, description TEXT PRIMARY KEY)')
    cur.execute('CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, user_id INT UNIQUE, name TEXT, phone_number TEXT, adress TEXT, commentary Text, tools_c INTEGER, obtaining TEXT, time_order TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS cart (id SERIAL PRIMARY KEY, user_id INT, product_id INT, count INT)')
    cur.execute('CREATE TABLE IF NOT EXISTS categories (category_name TEXT, category_id SERIAL PRIMARY KEY, availability_cat INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS orders_user (id SERIAL PRIMARY KEY, id_order INTEGER, user_id INTEGER, cart TEXT, order_date TEXT, receiving TEXT, status TEXT, payment TEXT, commentary TEXT)')
    base.commit()

def sql_add_start_date():
    # здесь вводим исходные данные бд для работоспособности
    cur.execute('INSERT INTO restaurant (location_time, img, description, price_obtain, limit_price, availability, availability_mess) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                ('Аша 18:00-23:00', 'AgACAgIAAxkBAAIUDWQ7JK9TKJo2QEqkqkLUMzU10-qbAAKtyDEbHj_ZSVa2kq2QMjf7AQADAgADcwADLwQ', 'туту', '200', '1150', '1', 'У нас много заказов, заказывайте завтра! Ок?)'))
    cur.execute('INSERT INTO promotion (img, name, description) VALUES (%s, %s, %s)', ('AgACAgIAAxkBAAIUDWQ7JK9TKJo2QEqkqkLUMzU10-qbAAKtyDEbHj_ZSVa2kq2QMjf7AQADAgADcwADLwQ', '0', 'туту'))
    cur.execute('INSERT INTO anonce(img, description) VALUES (%s, %s)', ('AgACAgIAAxkBAAIUDWQ7JK9TKJo2QEqkqkLUMzU10-qbAAKtyDEbHj_ZSVa2kq2QMjf7AQADAgADcwADLwQ', 'тут тут'))
    base.commit()

async def sql_start21():
    cur.execute('SELECT user_id FROM users')
    return cur.fetchall()

async def sql_start2(message):
    cur.execute('INSERT INTO users(user_id, name) VALUES (%s, %s)', (message.chat.id, message.chat.first_name,))
    base.commit()

'''********************Запросы к бд, при действии серии кнопок "Стоп_заказы"********************************'''

async def sql_stop_orders():
    cur.execute('UPDATE restaurant SET availability=(%s) WHERE id !=(%s)', [2, 0])
    base.commit()

async def sql_start_orders():
    cur.execute('UPDATE restaurant SET availability=(%s) WHERE id !=(%s)', [1, 0])
    base.commit()

async def sql_read_restaurant_for_availability():
    # return cur.execute('SELECT * FROM restaurant').fetchall()
    cur.execute('SELECT * FROM restaurant')
    return cur.fetchall()

async def sql_add_mess_for_availability(availability_mess):
    cur.execute("UPDATE restaurant SET availability_mess=(%s) WHERE id !=(%s)", (availability_mess, 0))
    base.commit()

async def sql_read_phone_numbers_user():
    # return cur.execute('SELECT * FROM users').fetchall()
    cur.execute('SELECT * FROM users')
    return cur.fetchall()

'''********************Запросы к бд, при действии серии кнопок "Работа_с_заказами"********************************'''

async def sql_add_order_client_nal(user_id, id_order, cart_order, order_date, status, payment):
    cur.execute('INSERT INTO orders_user(user_id, id_order, cart, order_date, status,payment) VALUES (%s, %s, %s, %s, %s, %s)', (user_id, id_order, cart_order, order_date, status, payment))
    base.commit()

async def sql_read_id_orders_user():
    # return cur.execute('SELECT * FROM orders_user').fetchall()
    cur.execute('SELECT * FROM orders_user')
    return cur.fetchall()

async def sql_read_id_orders_user_not_deliv():
    # return cur.execute('SELECT * FROM orders_user WHERE status="Не доставлен" ').fetchall()
    cur.execute("SELECT * FROM orders_user WHERE status = 'Не доставлен' ")
    return cur.fetchall()

async def sql_update_status_orders_user(id_order, receiving):
    cur.execute("""UPDATE orders_user SET status=(%s), receiving=(%s) WHERE id_order=(%s)""", ['Доставлен', receiving, id_order])
    base.commit()

async def sql_update_comment_orders_user(id_order, commentary):
    cur.execute("""UPDATE orders_user SET commentary=(%s) WHERE id_order=(%s)""", [commentary, id_order])
    base.commit()

async def sql_get_user_id_orders_client(id_order):
    # return cur.execute('SELECT * FROM orders_user WHERE id_order=(%s)', [id_order]).fetchall()
    cur.execute('SELECT * FROM orders_user WHERE id_order=(%s)', [id_order])
    return cur.fetchall()

async def sql_get_user_id_orders(user_id):
    # return cur.execute('SELECT * FROM orders_user WHERE user_id=(%s)', [user_id]).fetchall()
    cur.execute('SELECT * FROM orders_user WHERE user_id=(%s)', [user_id])
    return cur.fetchall()

'''********************Запросы к бд, при действии серии кнопок "Изменить_позицию_меню"********************************'''

async def sql_read_products(message):
    cur.execute('SELECT * FROM products')
    for ret in cur.fetchall():
        await bot.send_photo(message.from_user.id, ret[2], f'{ret[3]}\nОписание: {ret[4]}\nЦена {ret[5]}')

async def sql_read2_products():
    # return cur.execute('SELECT * FROM products').fetchall()
    cur.execute('SELECT * FROM products')
    return cur.fetchall()

async def sql_read3_products(user_id, product_id):
    # return cur.execute("""SELECT cart FROM cart WHERE user_id=(%s) AND product_id=(%s)""", [user_id, product_id]).fetchall()
    cur.execute("""SELECT cart FROM cart WHERE user_id=(%s) AND product_id=(%s)""", [user_id, product_id])
    return cur.fetchall()

async def sql_add_command_products(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO products (product_id, category_id, img, name, description, price, availability) VALUES (%s,%s,%s,%s,%s,%s,%s)', tuple(data.values()))
        base.commit()

async def sql_delete_command_products(data):
    cur.execute("DELETE FROM products WHERE id ==%s", (data,))
    base.commit()

async def sql_turn_off_products(product_id):
    cur.execute("""UPDATE products SET availability=(%s) WHERE product_id=(%s)""", [2, product_id])
    # cur.execute("DELETE FROM products WHERE id == ?", (data,))
    base.commit()

async def sql_turn_on_products(product_id):
    cur.execute("""UPDATE products SET availability=(%s) WHERE product_id=(%s)""", [1, product_id])
    # cur.execute("DELETE FROM products WHERE id == ?", (data,))
    base.commit()
'''***************** Логика кнопок "Загрузить_раздел_меню", "Удалить_раздел_меню" *****************'''

async def sql_turn_off_category(category_id):
    cur.execute("""UPDATE categories SET availability_cat=(%s) WHERE category_id=(%s)""", [2, category_id])
    # cur.execute("DELETE FROM products WHERE id == ?", (data,))
    base.commit()

async def sql_turn_on_category(category_id):
    cur.execute("""UPDATE categories SET availability_cat=(%s) WHERE category_id=(%s)""", [1, category_id])
    # cur.execute("DELETE FROM products WHERE id == ?", (data,))
    base.commit()

# достаёт все категории по кнопкам, для дальнейшего переключения по меню
async def get_categories_name():
    # return cur.execute("""SELECT category_name FROM categories""").fetchall()
    cur.execute("""SELECT category_name FROM categories""")
    return cur.fetchall()

async def sql_add_categories(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO categories(category_name, availability_cat) VALUES (%s,%s)', tuple(data.values()))
        base.commit()

async def sql_delete_category(data):
    cur.execute("DELETE FROM categories WHERE category_name =%s", (data,))
    base.commit()

'''********************Запросы к бд, при действии серии кнопок "Корзина"********************************'''

# достаём продукты определённой категории из корзины
async def get_products(category_id):
    # return cur.execute("""SELECT * FROM products WHERE category_id=(%s) AND availability ==1 """, [category_id]).fetchall()
    cur.execute("""SELECT * FROM products WHERE category_id=(%s) AND availability =1 """, [category_id])
    return cur.fetchall()

async def get_products_1(category_id, product_id):
    # return cur.execute("""SELECT * FROM products WHERE (category_id=(%s) AND availability ==1) AND product_id=(%s)""", (category_id, product_id)).fetchall()
    cur.execute("""SELECT * FROM products WHERE (category_id=(%s) AND availability =1) AND product_id=(%s)""", (category_id, product_id))
    return cur.fetchall()

# достаём конкретный продукт чтоб узнать его имя и цену
async def get_user_product(product_id):
    # return cur.execute("""SELECT * FROM products WHERE product_id=(%s)""", [product_id]).fetchall()
    cur.execute("""SELECT * FROM products WHERE product_id=(%s)""", [product_id])
    return cur.fetchall()

# достаём все продукты_айди для конкретного пользователя из корзины
async def get_cart(user_id):
    # return cur.execute("""SELECT * FROM cart WHERE user_id=(%s)""", [user_id]).fetchall()
    cur.execute("""SELECT * FROM cart WHERE user_id=(%s)""", [user_id])
    return cur.fetchall()

# срабатывает при нажатии на кнопку товара, чтоб добавить элемент в корзину и добавить 1 к количеству
async def add_to_cart(user_id, product_id):
    cur.execute('INSERT INTO cart (user_id, product_id, count) VALUES (%s,%s,%s)', (user_id, product_id, 1))
    base.commit()

# срабатывает при нажатии на кнопку очистки корзины
async def empty_cart(user_id):
    cur.execute("""DELETE FROM cart WHERE user_id=(%s)""", [user_id])
    base.commit()

# достаёт все категории по кнопкам, для дальнейшего переключения по меню
async def get_categories():
    # return cur.execute("""SELECT * FROM categories""").fetchall()
    # return cur.execute("""SELECT * FROM categories WHERE availability_cat ==1""").fetchall()
    cur.execute("""SELECT * FROM categories WHERE availability_cat = 1""")
    return cur.fetchall()

# достаёт все категории по кнопкам, для дальнейшего переключения по меню
async def get_all_categories():
    # return cur.execute("""SELECT * FROM categories""").fetchall()
    cur.execute("""SELECT * FROM categories""")
    return cur.fetchall()

async def get_all_products():
    # return cur.execute("""SELECT * FROM products""").fetchall()
    cur.execute("""SELECT * FROM products""")
    return cur.fetchall()

# достаём количество конретного товара у конкретного пользователя
async def get_count_in_cart(user_id, product_id):
    # return cur.execute("""SELECT count FROM cart WHERE user_id=(%s) AND product_id=(%s)""", [user_id, product_id]).fetchall()
    cur.execute("""SELECT count FROM cart WHERE user_id=(%s) AND product_id=(%s)""", [user_id, product_id])
    return cur.fetchall()

# очищаем корзину от конкретной позиции
async def remove_one_item(product_id, user_id):
    cur.execute("""DELETE FROM cart WHERE product_id=(%s) AND user_id=(%s)""", [product_id, user_id])
    base.commit()

# для кнопок + и - ,чтоб увеличивать или уменьшать количество товаров на единицу
async def change_count(count, product_id, user_id):
    cur.execute("""UPDATE cart SET count=(%s) WHERE product_id=(%s) AND user_id=(%s)""", [count, product_id, user_id])
    base.commit()

'''********************Запросы к бд, при действии серии кнопки "Добавить приборы на количество персон"********************************'''

async def sql_add_tools_c(tools_c, user_id):
    cur.execute("UPDATE users SET tools_c=(%s) WHERE user_id=(%s)", (tools_c, user_id))
    base.commit()

'''********************Запросы к бд, при действии серии кнопки "Время обработки заказа"********************************'''

async def sql_add_time_order(time_order, user_id):
    cur.execute("UPDATE users SET time_order=(%s) WHERE user_id=(%s)", (time_order, user_id))
    base.commit()

'''********************Запросы к бд, при действии серии кнопки "Способ получения заказа"********************************'''

async def sql_add_adress_c2(adress, obtaining, user_id):
    cur.execute("UPDATE users SET adress=(%s), obtaining=(%s) WHERE user_id=(%s)", (adress, obtaining, user_id))
    base.commit()

async def sql_add_obtaining_c2(obtaining, user_id):
    cur.execute("UPDATE users SET obtaining=(%s) WHERE user_id=(%s)", (obtaining, user_id))
    base.commit()

async def sql_get_obtaining(user_id):
    # return cur.execute("""SELECT * FROM users WHERE user_id=(%s)""", [user_id]).fetchall()
    cur.execute("""SELECT * FROM users WHERE user_id=(%s)""", [user_id])
    return cur.fetchall()

async def sql_get_limit_price_obtaining():
    # return cur.execute("""SELECT limit_price FROM restaurant""").fetchall()
    cur.execute("""SELECT limit_price FROM restaurant""")
    return cur.fetchall()

async def sql_get_price_obtaining():
    # return cur.execute("""SELECT price_obtain FROM restaurant""").fetchall()
    cur.execute("""SELECT price_obtain FROM restaurant""")
    return cur.fetchall()

async def sql_get_pickup_obtaining():
    # return cur.execute("""SELECT * FROM restaurant""").fetchall()
    cur.execute("""SELECT * FROM restaurant""")
    return cur.fetchall()

'''********************Запросы к бд, при действии серии кнопок "Новая_акция/скидка", "Удалить_акцию/скидку"********************************'''

async def sql_read_promotion(message):
    # for ret in cur.execute('SELECT * FROM promotion').fetchall():
    cur.execute('SELECT * FROM promotion')
    for ret in cur.fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n\n{ret[2]}')

async def sql_read2_promotion():
    # return cur.execute('SELECT * FROM promotion').fetchall()
    cur.execute('SELECT * FROM promotion')
    return cur.fetchall()

async def sql_add_command_promotion(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO promotion VALUES (%s,%s,%s)', tuple(data.values()))
        base.commit()

async def sql_delete_command_promotion(data):
    cur.execute("DELETE FROM promotion WHERE name = %s", (data,))
    base.commit()

'''********************Запросы к бд, при действии серии кнопки "Изменить_информацию_о_заведении"********************************'''

async def sql_read_restaurant(message):
    # for ret in cur.execute('SELECT location_time FROM restaurant;').fetchall():
    cur.execute('SELECT location_time FROM restaurant;')
    for ret in cur.fetchall():
        await bot.send_message(message.from_user.id, ret[0])

async def sql_add_restaurant(location_time):
    cur.execute("UPDATE restaurant SET location_time=(%s) WHERE id !=(%s)", (location_time, 0))
    base.commit()

async def sql_add_restaurant_pickup(img, description):
    cur.execute("UPDATE restaurant SET img=(%s), description=(%s) WHERE id !=(%s)", (img, description, 0))
    base.commit()

async def sql_add_restaurant_price_obtain(price_obtain):
    cur.execute("UPDATE restaurant SET price_obtain=(%s) WHERE id !=(%s)", (price_obtain, 0))
    base.commit()

async def sql_add_restaurant_limit_price(limit_price):
    cur.execute("UPDATE restaurant SET limit_price=(%s) WHERE id !=(%s)", (limit_price, 0))
    base.commit()

'''********************Запросы к бд, при действии серии кнопок "Сделать_объявление"********************************'''

async def sql_read_anonce(message):
    # for ret in cur.execute('SELECT * FROM anonce').fetchall():
    cur.execute('SELECT * FROM anonce')
    for ret in cur.fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}')

async def sql_read2_anonce():
    # return cur.execute('SELECT * FROM anonce').fetchall()
    cur.execute('SELECT * FROM anonce')
    return cur.fetchall()

async def sql_add_command_anonce(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO anonce VALUES (%s,%s)', tuple(data.values()))
        base.commit()

async def sql_anonce(message):
    # for ret in cur.execute('SELECT * FROM anonce').fetchall():
    cur.execute('SELECT * FROM anonce')
    for ret in cur.fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}')

async def sql_delete_command_anonce(data):
    cur.execute("DELETE FROM anonce WHERE description =%s", (data,))
    base.commit()

async def sql_read2_users():
    # return cur.execute('SELECT * FROM users').fetchall()
    cur.execute('SELECT * FROM users')
    return cur.fetchall()

async def sql_read3_users():
    # return cur.execute('SELECT user_id FROM users').fetchall()
    cur.execute('SELECT user_id FROM users')
    return cur.fetchall()

'''********************Запросы к бд, при действии серии кнопки "Изменить_мои_данные"********************************'''

async def get_myself(user_id):
    # return cur.execute('SELECT * FROM users WHERE user_id=(%s)', [user_id]).fetchall()
    cur.execute('SELECT * FROM users WHERE user_id=(%s)', [user_id])
    return cur.fetchall()

async def sql_add_name_c(name_c, user_id):
    cur.execute("UPDATE users SET name=(%s) WHERE user_id=(%s)", (name_c, user_id))
    base.commit()

async def sql_add_number_c(number_c, user_id):
    cur.execute("UPDATE users SET phone_number=(%s) WHERE user_id=(%s)", (number_c, user_id))
    base.commit()

async def sql_add_adress_c(adress_c, user_id):
    cur.execute("UPDATE users SET adress=(%s) WHERE user_id=(%s)", (adress_c, user_id))
    base.commit()

async def sql_add_commentary_c(commentary_c, user_id):
    cur.execute("UPDATE users SET commentary=(%s) WHERE user_id=(%s)", (commentary_c, user_id))
    base.commit()

