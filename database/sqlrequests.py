from database.models import User, Product, Category, Cart, OrdersUser, Restaurant, Promotion, Anonce
from database.connect import SessionLocal

# Добавление данных начальной базы
def sql_try_fixtures():
    with SessionLocal() as session:
        # Создание ресторанов
        restaurant = Restaurant(
            location_time='Аша 18:00-23:00',
            img='AgACAgIAAxkBAAIUDWQ7JK9TKJo2QEqkqkLUMzU10-qbAAKtyDEbHj_ZSVa2kq2QMjf7AQADAgADcwADLwQ',
            description='туту',
            price_obtain=200,
            limit_price=1150,
            availability=1,
            availability_mess='У нас много заказов, заказывайте завтра! Ок?)'
        )
        session.add(restaurant)
        session.commit()

        # Создание акций
        promotion = Promotion(
            img='AgACAgIAAxkBAAIUDWQ7JK9TKJo2QEqkqkLUMzU10-qbAAKtyDEbHj_ZSVa2kq2QMjf7AQADAgADcwADLwQ',
            name='0',
            description='туту'
        )
        session.add(promotion)
        session.commit()

        # Создание анонсов
        anonce = Anonce(
            img='AgACAgIAAxkBAAIUDWQ7JK9TKJo2QEqkqkLUMzU10-qbAAKtyDEbHj_ZSVa2kq2QMjf7AQADAgADcwADLwQ',
            description='тут тут'
        )
        session.add(anonce)
        session.commit()  # Сохраняем всё в базе


async def sql_start21():
    """Возвращает все user_id из пользователей."""
    with SessionLocal() as session:
        result = session.query(User.user_id).all()
        return result


async def sql_start2(message):
    """Добавляет нового пользователя по его id и имени."""
    with SessionLocal() as session:
        user = User(user_id=message.chat.id, name=message.chat.first_name)
        session.add(user)
        session.commit()


async def sql_stop_orders():
    """Отключает заказы в ресторанах."""
    with SessionLocal() as session:
        session.query(Restaurant).update({"availability": 2}, synchronize_session='fetch')
        session.commit()


async def sql_start_orders():
    """Включает заказы в ресторанах."""
    with SessionLocal() as session:
        session.query(Restaurant).update({"availability": 1}, synchronize_session='fetch')
        session.commit()


async def sql_read_restaurant_for_availability():
    """Возвращает все рестораны из базы данных."""
    with SessionLocal() as session:
        return session.query(Restaurant).all()


async def sql_add_mess_for_availability(availability_mess):
    """Обновляет сообщение о доступности ресторанов."""
    with SessionLocal() as session:
        session.query(Restaurant).update({"availability_mess": availability_mess}, synchronize_session='fetch')
        session.commit()


async def sql_read_phone_numbers_user():
    """Возвращает все номера телефонов пользователей."""
    with SessionLocal() as session:
        return session.query(User.phone_number).all()


async def sql_add_order_client_nal(user_id, id_order, cart_order, order_date, status, payment):
    """Добавляет новый заказ для клиента."""
    with SessionLocal() as session:
        order = OrdersUser(
            user_id=user_id,
            id_order=id_order,
            cart=cart_order,
            order_date=order_date,
            status=status,
            payment=payment
        )
        session.add(order)
        session.commit()


async def sql_read_id_orders_user():
    """Возвращает все заказы пользователей."""
    with SessionLocal() as session:
        return session.query(OrdersUser).all()


async def sql_read_id_orders_user_not_deliv():
    """Возвращает заказы пользователей со статусом 'Не доставлен'."""
    with SessionLocal() as session:
        return session.query(OrdersUser).filter(OrdersUser.status == "Не доставлен").all()


async def sql_update_status_orders_user(id_order, receiving):
    """Обновляет статус заказа пользователя."""
    with SessionLocal() as session:
        session.query(OrdersUser).filter(OrdersUser.id_order == id_order).update({
            "status": 'Доставлен',
            "receiving": receiving
        }, synchronize_session='fetch')
        session.commit()


async def sql_update_comment_orders_user(id_order, commentary):
    """Обновляет комментарий заказа пользователя."""
    with SessionLocal() as session:
        session.query(OrdersUser).filter(OrdersUser.id_order == id_order).update({
            "commentary": commentary
        }, synchronize_session='fetch')
        session.commit()


async def sql_get_user_id_orders_client(id_order):
    """Возвращает информацию о заказе клиента по id заказа."""
    with SessionLocal() as session:
        return session.query(OrdersUser).filter(OrdersUser.id_order == id_order).all()


async def sql_get_user_id_orders(user_id):
    """Возвращает все заказы пользователя по его user_id."""
    with SessionLocal() as session:
        return session.query(OrdersUser).filter(OrdersUser.user_id == user_id).all()


# async def sql_read_products(message):
#     """Отправляет пользователю информацию о всех продуктах."""
#     with SessionLocal() as session:
#         products = session.query(Product).all()
#         for product in products:
#             await bot.send_photo(message.from_user.id, product.img, f'{product.name}\nОписание: {product.description}\nЦена {product.price}')


async def sql_read2_products():
    """Возвращает все продукты."""
    with SessionLocal() as session:
        return session.query(Product).all()


async def sql_read3_products(user_id, product_id):
    """Возвращает количество товара в корзине для конкретного пользователя и продукта."""
    with SessionLocal() as session:
        return session.query(Cart.cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).all()


async def sql_add_command_products(state):
    """Добавляет новый продукт в базу данных."""
    async with state.proxy() as data:
        product = Product(**data)
        with SessionLocal() as session:
            session.add(product)
            session.commit()


async def sql_delete_command_products(data):
    """Удаляет продукт из базы данных по id."""
    with SessionLocal() as session:
        session.query(Product).filter(Product.id == data).delete()
        session.commit()


async def sql_turn_off_products(product_id):
    """Выключает продукт в базе данных."""
    with SessionLocal() as session:
        session.query(Product).filter(Product.product_id == product_id).update({"availability": 2}, synchronize_session='fetch')
        session.commit()


async def sql_turn_on_products(product_id):
    """Включает продукт в базе данных."""
    with SessionLocal() as session:
        session.query(Product).filter(Product.product_id == product_id).update({"availability": 1}, synchronize_session='fetch')
        session.commit()


async def sql_turn_off_category(category_id):
    """Выключает категорию в базе данных."""
    with SessionLocal() as session:
        session.query(Category).filter(Category.category_id == category_id).update({"availability_cat": 2}, synchronize_session='fetch')
        session.commit()


async def sql_turn_on_category(category_id):
    """Включает категорию в базе данных."""
    with SessionLocal() as session:
        session.query(Category).filter(Category.category_id == category_id).update({"availability_cat": 1}, synchronize_session='fetch')
        session.commit()


async def get_categories_name():
    """Возвращает все названия категорий."""
    with SessionLocal() as session:
        return session.query(Category.category_name).all()


async def sql_add_categories(state):
    """Добавляет новую категорию в базу данных."""
    async with state.proxy() as data:
        category = Category(**data)
        with SessionLocal() as session:
            session.add(category)
            session.commit()


async def sql_delete_category(data):
    """Удаляет категорию по названию."""
    with SessionLocal() as session:
        session.query(Category).filter(Category.category_name == data).delete()
        session.commit()


async def get_products(category_id):
    """Возвращает все продукты определённой категории."""
    with SessionLocal() as session:
        return session.query(Product).filter(Product.category_id == category_id, Product.availability == 1).all()


async def get_products_1(category_id, product_id):
    """Возвращает продукт по ID и категории."""
    with SessionLocal() as session:
        return session.query(Product).filter(Product.category_id == category_id, Product.product_id == product_id, Product.availability == 1).all()


async def get_user_product(product_id):
    """Возвращает продукт по product_id."""
    with SessionLocal() as session:
        return session.query(Product).filter(Product.product_id == product_id).all()


async def get_cart(user_id):
    """Возвращает все продукты в корзине конкретного пользователя."""
    with SessionLocal() as session:
        return session.query(Cart).filter(Cart.user_id == user_id).all()


async def add_to_cart(user_id, product_id):
    """Добавляет товар в корзину."""
    with SessionLocal() as session:
        cart_item = Cart(user_id=user_id, product_id=product_id, count=1)
        session.add(cart_item)
        session.commit()


async def empty_cart(user_id):
    """Очищает корзину конкретного пользователя."""
    with SessionLocal() as session:
        session.query(Cart).filter(Cart.user_id == user_id).delete()
        session.commit()


async def get_categories():
    """Возвращает все категории с доступностью 1."""
    with SessionLocal() as session:
        return session.query(Category).filter(Category.availability_cat == 1).all()


async def get_all_categories():
    """Возвращает все категории."""
    with SessionLocal() as session:
        return session.query(Category).all()


async def get_all_products():
    """Возвращает все продукты."""
    with SessionLocal() as session:
        return session.query(Product).all()


async def get_count_in_cart(user_id, product_id):
    """Возвращает количество товара в корзине."""
    with SessionLocal() as session:
        return session.query(Cart.count).filter(Cart.user_id == user_id, Cart.product_id == product_id).all()


async def remove_one_item(product_id, user_id):
    """Удаляет конкретный товар из корзины."""
    with SessionLocal() as session:
        session.query(Cart).filter(Cart.product_id == product_id, Cart.user_id == user_id).delete()
        session.commit()


async def change_count(count, product_id, user_id):
    """Изменяет количество товара в корзине."""
    with SessionLocal() as session:
        session.query(Cart).filter(Cart.product_id == product_id, Cart.user_id == user_id).update({"count": count}, synchronize_session='fetch')
        session.commit()


async def sql_add_tools_c(tools_c, user_id):
    """Обновляет количество приборов у пользователя."""
    with SessionLocal() as session:
        session.query(User).filter(User.user_id == user_id).update({"tools_c": tools_c}, synchronize_session='fetch')
        session.commit()


async def sql_add_time_order(time_order, user_id):
    """Обновляет время заказа у пользователя."""
    with SessionLocal() as session:
        session.query(User).filter(User.user_id == user_id).update({"time_order": time_order}, synchronize_session='fetch')
        session.commit()


async def sql_add_adress_c2(adress, obtaining, user_id):
    """Обновляет адрес и способ получения заказа у пользователя."""
    with SessionLocal() as session:
        session.query(User).filter(User.user_id == user_id).update({"adress": adress, "obtaining": obtaining}, synchronize_session='fetch')
        session.commit()


async def sql_add_obtaining_c2(obtaining, user_id):
    """Обновляет способ получения заказа у пользователя."""
    with SessionLocal() as session:
        session.query(User).filter(User.user_id == user_id).update({"obtaining": obtaining}, synchronize_session='fetch')
        session.commit()


async def sql_get_obtaining(user_id):
    """Возвращает способ получения заказа у пользователя."""
    with SessionLocal() as session:
        return session.query(User).filter(User.user_id == user_id).all()


async def sql_get_limit_price_obtaining():
    """Возвращает лимит по ценам получения ресторана."""
    with SessionLocal() as session:
        return session.query(Restaurant.limit_price).all()


async def sql_get_price_obtaining():
    """Возвращает цену получения ресторана."""
    with SessionLocal() as session:
        return session.query(Restaurant.price_obtain).all()


async def sql_get_pickup_obtaining():
    """Возвращает все рестораны."""
    with SessionLocal() as session:
        return session.query(Restaurant).all()


async def sql_read_promotion():
    """Отправляет пользователю информацию о всех промоциях."""
    with SessionLocal() as session:
        return session.query(Promotion).all()


async def sql_read2_promotion():
    """Возвращает все промоции."""
    with SessionLocal() as session:
        return session.query(Promotion).all()


async def sql_add_command_promotion(state):
    """Добавляет новую промоцию в базу данных."""
    async with state.proxy() as data:
        promotion = Promotion(**data)
        with SessionLocal() as session:
            session.add(promotion)
            session.commit()


async def sql_delete_command_promotion(data):
    """Удаляет промоцию по названию."""
    with SessionLocal() as session:
        session.query(Promotion).filter(Promotion.name == data).delete()
        session.commit()


async def sql_read_restaurant():
    """Отправляет пользователю информацию о времени работы ресторанов."""
    with SessionLocal() as session:
        return session.query(Restaurant.location_time).all()


async def sql_add_restaurant(location_time):
    """Обновляет время работы ресторана."""
    with SessionLocal() as session:
        session.query(Restaurant).update({"location_time": location_time}, synchronize_session='fetch')
        session.commit()


async def sql_add_restaurant_pickup(img, description):
    """Обновляет изображение и описание ресторана."""
    with SessionLocal() as session:
        session.query(Restaurant).update({"img": img, "description": description}, synchronize_session='fetch')
        session.commit()


async def sql_add_restaurant_price_obtain(price_obtain):
    """Обновляет цену получения у ресторана."""
    with SessionLocal() as session:
        session.query(Restaurant).update({"price_obtain": price_obtain}, synchronize_session='fetch')
        session.commit()


async def sql_add_restaurant_limit_price(limit_price):
    """Обновляет лимит цены у ресторана."""
    with SessionLocal() as session:
        session.query(Restaurant).update({"limit_price": limit_price}, synchronize_session='fetch')
        session.commit()


async def sql_read2_anonce():
    """Возвращает все анонсы."""
    with SessionLocal() as session:
        return session.query(Anonce).all()


async def sql_add_command_anonce(state):
    """Добавляет новый анонс в базу данных."""
    async with state.proxy() as data:
        anonce = Anonce(**data)
        with SessionLocal() as session:
            session.add(anonce)
            session.commit()


async def sql_delete_command_anonce(data):
    """Удаляет анонс по описанию."""
    with SessionLocal() as session:
        session.query(Anonce).filter(Anonce.description == data).delete()
        session.commit()


async def sql_read2_users():
    """Возвращает всех пользователей."""
    with SessionLocal() as session:
        return session.query(User).all()


async def sql_read3_users():
    """Возвращает все user_id пользователей."""
    with SessionLocal() as session:
        return session.query(User.user_id).all()


async def get_myself(user_id):
    """Возвращает информацию о пользователе по user_id."""
    with SessionLocal() as session:
        return session.query(User).filter(User.user_id == user_id).all()


async def sql_add_name_c(name_c, user_id):
    """Обновляет имя пользователя."""
    with SessionLocal() as session:
        session.query(User).filter(User.user_id == user_id).update({"name": name_c}, synchronize_session='fetch')
        session.commit()


async def sql_add_number_c(number_c, user_id):
    """Обновляет номер телефона пользователя."""
    with SessionLocal() as session:
        session.query(User).filter(User.user_id == user_id).update({"phone_number": number_c}, synchronize_session='fetch')
        session.commit()


async def sql_add_adress_c(adress_c, user_id):
    """Обновляет адрес пользователя."""
    with SessionLocal() as session:
        session.query(User).filter(User.user_id == user_id).update({"adress": adress_c}, synchronize_session='fetch')
        session.commit()


async def sql_add_commentary_c(commentary_c, user_id):
    """Обновляет комментарий пользователя."""
    with SessionLocal() as session:
        session.query(User).filter(User.user_id == user_id).update({"commentary": commentary_c}, synchronize_session='fetch')
        session.commit()

