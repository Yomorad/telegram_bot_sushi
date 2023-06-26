from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Кнопки клавиатуры админа
button_categories = KeyboardButton('/Изменить_категории')
button_products = KeyboardButton('/Изменить_позицию_меню')
button_restaurant = KeyboardButton('/Изменить_данные_ресторана')
button_promotion = KeyboardButton('/Акция/скидка')
button_notify = KeyboardButton('/Сделать_объявление')
button_orders = KeyboardButton('/Работа_с_заказами')
button_user = KeyboardButton('/Режим_пользователя')
button_availability = KeyboardButton('/Стоп_заказы')
button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(button_categories, button_products)\
    .row(button_restaurant, button_notify).row(button_promotion, button_orders).row(button_availability, button_user)

l1 = KeyboardButton('/Включить_заказы')
l2 = KeyboardButton('/Выключить_заказы')
l3 = KeyboardButton('/Сообщение_для_пользователя')
l4 = KeyboardButton('/Меню_модератора')
kb_admin_availability = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_admin_availability.row(l1, l2).row(l3, l4)

t1 = KeyboardButton('/Новая_акция/скидка')
t2 = KeyboardButton('/Удалить_акцию_скидку')
t3 = KeyboardButton('/Меню_модератора')
kb_admin_promotion = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_admin_promotion.row(t1, t2).row(t3)

h1 = KeyboardButton('/Добавить_категорию')
h2 = KeyboardButton('/Удалить_категорию')
h3 = KeyboardButton('/Стоп_Вкл_категория')
h4 = KeyboardButton('/Меню_модератора')
kb_admin_cat = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_admin_cat.row(h1, h2).row(h3, h4)

u1 = KeyboardButton('/Изменить_информацию_о_заведении')
u2 = KeyboardButton('/Изменить_информацию_о_самовывозе')
u3 = KeyboardButton('/Изменить_цену_доставки')
u4 = KeyboardButton('/Изменить_предел_цены_бесплатной_доставки')
u5 = KeyboardButton('/Меню_модератора')
kb_admin_restaurant = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_admin_restaurant.row(u1, u2).row(u3, u4).row(u5)

r1 = KeyboardButton('/Добавить_позицию_меню')
r2 = KeyboardButton('/Удалить_позицию_меню')
r3 = KeyboardButton('/Стоп_Вкл_позиция')
r4 = KeyboardButton('/Меню_модератора')
kb_admin_pos = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_admin_pos.row(r1, r2).row(r3, r4)

y1 = KeyboardButton('/Создать_объявление')
y2 = KeyboardButton('/Объявить_или_удалить_объявление')
y3 = KeyboardButton('/Меню_модератора')
kb_admin_anounce = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_admin_anounce.row(y1, y2).row(y3)

s1 = KeyboardButton('/Подтвердить_доставку_заказа')
s2 = KeyboardButton('/Комментарий_к_заказу')
s3 = KeyboardButton('/Заказы_клиента')
s4 = KeyboardButton('/Посмотреть_заказ')
s5 = KeyboardButton('/Меню_модератора')
kb_admin_orders = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_admin_orders.row(s1, s2).row(s3, s4).row(s5)