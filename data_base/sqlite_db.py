
import sqlite3 as sq
from create_bot import bot

# создаём если нет таблицы с нужными параметрами, кидаем оповещение в консоли
def sql_start():
    global base, cur
    base = sq.connect('sushi.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK')
    base.execute('CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER UNIQUE, img TEXT, name TEXT, description TEXT, price INT, category_id INT, availability INTEGER)')
    base.execute("CREATE TABLE IF NOT EXISTS restaurant(id INTEGER PRIMARY KEY AUTOINCREMENT, location_time TEXT, img TEXT, description TEXT, price_obtain INTEGER, limit_price INTEGER, availability INTEGER, availability_mess TEXT)")
    base.execute('CREATE TABLE IF NOT EXISTS promotion(img TEXT, name TEXT PRIMARY KEY, description TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS anonce(img TEXT, description TEXT PRIMARY KEY)')
    base.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT UNIQUE ON CONFLICT IGNORE, name TEXT, phone_number TEXT, adress TEXT, commentary Text, tools_c INTEGER, obtaining TEXT, time_order TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, product_id INT, count INT)')
    base.execute('CREATE TABLE IF NOT EXISTS categories (category_name TEXT, category_id INTEGER PRIMARY KEY AUTOINCREMENT, availability_cat INTEGER)')
    base.execute( 'CREATE TABLE IF NOT EXISTS orders_user (id INTEGER PRIMARY KEY AUTOINCREMENT, id_order INTEGER, user_id INTEGER, cart TEXT, order_date TEXT, receiving TEXT, status TEXT, payment TEXT, commentary TEXT)')
    base.commit()

async def sql_start2(message):
    cur.execute('INSERT INTO users(user_id, name) VALUES (?, ?)', (message.chat.id, message.chat.first_name))
    base.commit()

'''********************Запросы к бд, при действии серии кнопок "Стоп_заказы"********************************'''

async def sql_stop_orders():
    cur.execute('UPDATE restaurant SET availability=(?) WHERE id !=(?)', [2, 0])
    base.commit()

async def sql_start_orders():
    cur.execute('UPDATE restaurant SET availability=(?) WHERE id !=(?)', [1, 0])
    base.commit()

async def sql_read_restaurant_for_availability():
    return cur.execute('SELECT * FROM restaurant').fetchall()

async def sql_add_mess_for_availability(availability_mess):
    cur.execute("UPDATE restaurant SET availability_mess=(?) WHERE id !=(?)", (availability_mess, 0))
    base.commit()

async def sql_read_phone_numbers_user():
    return cur.execute('SELECT * FROM users').fetchall()

'''********************Запросы к бд, при действии серии кнопок "Работа_с_заказами"********************************'''

async def sql_add_order_client_nal(user_id, id_order, cart_order, order_date, status, payment):
    cur.execute('INSERT INTO orders_user(user_id, id_order, cart, order_date, status,payment) VALUES (?, ?, ?, ?, ?, ?)', (user_id, id_order, cart_order, order_date, status,payment))
    base.commit()

async def sql_read_id_orders_user():
    return cur.execute('SELECT * FROM orders_user').fetchall()

async def sql_read_id_orders_user_not_deliv():
    return cur.execute('SELECT * FROM orders_user WHERE status="Не доставлен" ').fetchall()

async def sql_update_status_orders_user(id_order, receiving):
    cur.execute("""UPDATE orders_user SET status=(?), receiving=(?) WHERE id_order=(?)""", ['Доставлен', receiving, id_order])
    base.commit()

async def sql_update_comment_orders_user(id_order, commentary):
    cur.execute("""UPDATE orders_user SET commentary=(?) WHERE id_order=(?)""", [commentary, id_order])
    base.commit()

async def sql_get_user_id_orders_client(id_order):
    return cur.execute('SELECT * FROM orders_user WHERE id_order=(?)', [id_order]).fetchall()

async def sql_get_user_id_orders(user_id):
    return cur.execute('SELECT * FROM orders_user WHERE user_id=(?)', [user_id]).fetchall()

'''********************Запросы к бд, при действии серии кнопок "Изменить_позицию_меню"********************************'''

async def sql_read_products(message):
    for ret in cur.execute('SELECT * FROM products').fetchall():
        await bot.send_photo(message.from_user.id, ret[2], f'{ret[3]}\nОписание: {ret[4]}\nЦена {ret[5]}')

async def sql_read2_products():
    return cur.execute('SELECT * FROM products').fetchall()

async def sql_read3_products(user_id, product_id):
    return cur.execute("""SELECT cart FROM cart WHERE user_id=(?) AND product_id=(?)""", [user_id, product_id]).fetchall()

async def sql_add_command_products(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO products (product_id, category_id, img, name, description, price, availability) VALUES (?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_delete_command_products(data):
    cur.execute("DELETE FROM products WHERE id == ?", (data,))
    base.commit()

async def sql_turn_off_products(product_id):
    cur.execute("""UPDATE products SET availability=(?) WHERE product_id=(?)""", [2, product_id])
    # cur.execute("DELETE FROM products WHERE id == ?", (data,))
    base.commit()

async def sql_turn_on_products(product_id):
    cur.execute("""UPDATE products SET availability=(?) WHERE product_id=(?)""", [1, product_id])
    # cur.execute("DELETE FROM products WHERE id == ?", (data,))
    base.commit()
'''***************** Логика кнопок "Загрузить_раздел_меню", "Удалить_раздел_меню" *****************'''

async def sql_turn_off_category(category_id):
    cur.execute("""UPDATE categories SET availability_cat=(?) WHERE category_id=(?)""", [2, category_id])
    # cur.execute("DELETE FROM products WHERE id == ?", (data,))
    base.commit()

async def sql_turn_on_category(category_id):
    cur.execute("""UPDATE categories SET availability_cat=(?) WHERE category_id=(?)""", [1, category_id])
    # cur.execute("DELETE FROM products WHERE id == ?", (data,))
    base.commit()

# достаёт все категории по кнопкам, для дальнейшего переключения по меню
async def get_categories_name():
    return cur.execute("""SELECT category_name FROM categories""").fetchall()

async def sql_add_categories(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO categories(category_name, availability_cat) VALUES (?, ?)', tuple(data.values()))
        base.commit()

async def sql_delete_category(data):
    cur.execute("DELETE FROM categories WHERE category_name == ?", (data,))
    base.commit()

'''********************Запросы к бд, при действии серии кнопок "Корзина"********************************'''

# достаём продукты определённой категории из корзины
async def get_products(category_id):
    return cur.execute("""SELECT * FROM products WHERE category_id=(?) AND availability ==1 """, [category_id]).fetchall()

async def get_products_1(category_id, product_id):
    return cur.execute("""SELECT * FROM products WHERE (category_id=(?) AND availability ==1) AND product_id=(?)""",
                       (category_id, product_id)).fetchall()

# достаём конкретный продукт чтоб узнать его имя и цену
async def get_user_product(product_id):
    return cur.execute("""SELECT * FROM products WHERE product_id=(?)""", [product_id]).fetchall()

# достаём все продукты_айди для конкретного пользователя из корзины
async def get_cart(user_id):
    return cur.execute("""SELECT * FROM cart WHERE user_id=(?)""", [user_id]).fetchall()

# срабатывает при нажатии на кнопку товара, чтоб добавить элемент в корзину и добавить 1 к количеству
async def add_to_cart(user_id, product_id):
    cur.execute('INSERT INTO cart (user_id, product_id, count) VALUES (?, ?, ?)', (user_id, product_id, 1))
    base.commit()

# срабатывает при нажатии на кнопку очистки корзины
async def empty_cart(user_id):
    cur.execute("""DELETE FROM cart WHERE user_id=(?)""", [user_id])
    base.commit()

# достаёт все категории по кнопкам, для дальнейшего переключения по меню
async def get_categories():
    # return cur.execute("""SELECT * FROM categories""").fetchall()
    return cur.execute("""SELECT * FROM categories WHERE availability_cat ==1""").fetchall()

# достаёт все категории по кнопкам, для дальнейшего переключения по меню
async def get_all_categories():
    return cur.execute("""SELECT * FROM categories""").fetchall()

async def get_all_products():
    return cur.execute("""SELECT * FROM products""").fetchall()

# достаём количество конретного товара у конкретного пользователя
async def get_count_in_cart(user_id, product_id):
    return cur.execute("""SELECT count FROM cart WHERE user_id=(?) AND product_id=(?)""", [user_id, product_id]).fetchall()

# очищаем корзину от конкретной позиции
async def remove_one_item(product_id, user_id):
    cur.execute("""DELETE FROM cart WHERE product_id=(?) AND user_id=(?)""", [product_id, user_id])
    base.commit()

# для кнопок + и - ,чтоб увеличивать или уменьшать количество товаров на единицу
async def change_count(count, product_id, user_id):
    cur.execute("""UPDATE cart SET count=(?) WHERE product_id=(?) AND user_id=(?)""", [count, product_id, user_id])
    base.commit()

'''********************Запросы к бд, при действии серии кнопки "Добавить приборы на количество персон"********************************'''

async def sql_add_tools_c(tools_c, user_id):
    cur.execute("UPDATE users SET tools_c=(?) WHERE user_id=(?)", (tools_c, user_id))
    base.commit()

'''********************Запросы к бд, при действии серии кнопки "Время обработки заказа"********************************'''

async def sql_add_time_order(time_order, user_id):
    cur.execute("UPDATE users SET time_order=(?) WHERE user_id=(?)", (time_order, user_id))
    base.commit()

'''********************Запросы к бд, при действии серии кнопки "Способ получения заказа"********************************'''

async def sql_add_adress_c2(adress, obtaining, user_id):
    cur.execute("UPDATE users SET adress=(?), obtaining=(?) WHERE user_id=(?)", (adress, obtaining, user_id))
    base.commit()

async def sql_add_obtaining_c2(obtaining, user_id):
    cur.execute("UPDATE users SET obtaining=(?) WHERE user_id=(?)", (obtaining, user_id))
    base.commit()

async def sql_get_obtaining(user_id):
    return cur.execute("""SELECT * FROM users WHERE user_id=(?)""", [user_id]).fetchall()

async def sql_get_limit_price_obtaining():
    return cur.execute("""SELECT limit_price FROM restaurant""").fetchall()

async def sql_get_price_obtaining():
    return cur.execute("""SELECT price_obtain FROM restaurant""").fetchall()

async def sql_get_pickup_obtaining():
    return cur.execute("""SELECT * FROM restaurant""").fetchall()

'''********************Запросы к бд, при действии серии кнопок "Новая_акция/скидка", "Удалить_акцию/скидку"********************************'''

async def sql_read_promotion(message):
    for ret in cur.execute('SELECT * FROM promotion').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n\n{ret[2]}')

async def sql_read2_promotion():
    return cur.execute('SELECT * FROM promotion').fetchall()

async def sql_add_command_promotion(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO promotion VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_delete_command_promotion(data):
    cur.execute("DELETE FROM promotion WHERE name == ?", (data,))
    base.commit()

'''********************Запросы к бд, при действии серии кнопки "Изменить_информацию_о_заведении"********************************'''

async def sql_read_restaurant(message):
    for ret in cur.execute('SELECT location_time FROM restaurant').fetchall():
        await bot.send_message(message.from_user.id, ret[0])

async def sql_add_restaurant(location_time):
    cur.execute("UPDATE restaurant SET location_time=(?) WHERE id !=(?)", (location_time, 0))
    base.commit()

async def sql_add_restaurant_pickup(img, description):
    cur.execute("UPDATE restaurant SET img=(?), description=(?) WHERE id !=(?)", (img, description, 0))
    base.commit()

async def sql_add_restaurant_price_obtain(price_obtain):
    cur.execute("UPDATE restaurant SET price_obtain=(?) WHERE id !=(?)", (price_obtain, 0))
    base.commit()

async def sql_add_restaurant_limit_price(limit_price):
    cur.execute("UPDATE restaurant SET limit_price=(?) WHERE id !=(?)", (limit_price, 0))
    base.commit()

'''********************Запросы к бд, при действии серии кнопок "Сделать_объявление"********************************'''

async def sql_read_anonce(message):
    for ret in cur.execute('SELECT * FROM anonce').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}')

async def sql_read2_anonce():
    return cur.execute('SELECT * FROM anonce').fetchall()

async def sql_add_command_anonce(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO anonce VALUES (?, ?)', tuple(data.values()))
        base.commit()

async def sql_anonce(message):
    for ret in cur.execute('SELECT * FROM anonce').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}')

async def sql_delete_command_anonce(data):
    cur.execute("DELETE FROM anonce WHERE description == ?", (data,))
    base.commit()

async def sql_read2_users():
    return cur.execute('SELECT * FROM users').fetchall()

async def sql_read3_users():
    return cur.execute('SELECT user_id FROM users').fetchall()

'''********************Запросы к бд, при действии серии кнопки "Изменить_мои_данные"********************************'''

async def get_myself(user_id):
    return cur.execute('SELECT * FROM users WHERE user_id=(?)', [user_id]).fetchall()

async def sql_add_name_c(name_c, user_id):
    cur.execute("UPDATE users SET name=(?) WHERE user_id=(?)", (name_c, user_id))
    base.commit()

async def sql_add_number_c(number_c, user_id):
    cur.execute("UPDATE users SET phone_number=(?) WHERE user_id=(?)", (number_c, user_id))
    base.commit()

async def sql_add_adress_c(adress_c, user_id):
    cur.execute("UPDATE users SET adress=(?) WHERE user_id=(?)", (adress_c, user_id))
    base.commit()

async def sql_add_commentary_c(commentary_c, user_id):
    cur.execute("UPDATE users SET commentary=(?) WHERE user_id=(?)", (commentary_c, user_id))
    base.commit()

