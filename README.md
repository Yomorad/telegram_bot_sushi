<h1 align="center">Hi there, This is a fully automated bot for an online store.
<img src="https://github.com/Yomorad/yomorad/blob/main/icons/pantsu-konosuba.gif" height="90"/></h1>

Автоматизированный бот для онлайн-магазина

Особенности:
1) доступ в админку только для указанного в config.py id пользователя
2) Все обработчики событий указаны в handlers:
    admin.py    обработчик событий админа
    client.py   обработчик событий пользователя
3) Все запросы к бд на PostgreSQL указаны в postgres_db.py
    данные для входа указаны в config.py
    инициалиализация и предзагрузка бд указана в on_startup() в bot_suchi.py
    все запросы разбиты по разделам
4) кнопки или инлайн-кнопки указаны в keyboards
    admin_kb.py    кнопки админа
    client_kb.py   кнопки пользователя
5) защита от спама указана в middlewares/throttling.py
6) Перед деплоем на сервер, обратите внимание на polling в точке входа и замените на webhook

Как осуществляется доступ в админку:
1) создаётся закрытая группа, куда добавляется админ-пользователь и бот
2) Админка открывается при команде /moderator при условии если id пользователя == id админа

Пояснение config.py:
1) Токен бота, выдающийся BotFather при регистрации
token: str = 'token' 
2) id админа, который бот зарегистрирует в бд при первом обращении, как обычного пользователя
admin_ids: int = 'admin_ids'
3) платёжный токен, выдаваемый BotFather через разделы оплаты, либо напрямую от банка через онлайн-эквайринг
pay_token: str = 'pay_token'
4) Базовые данные входа в бд PostgreSQL:
    data_base_p: str = 'data_base_p'
    user_p: str = 'user_p'
    host_p: str = 'host_p'
    password_p: str = 'password_p'
