<h1 align="center">Hi there, This is a telegram bot for an online store
<img src="https://github.com/Yomorad/yomorad/blob/main/icons/pantsu-konosuba.gif" height="90"/></h1>

### Телеграмм бот для онлайн-магазина
<p>bot_sushi.py - точка входа</p>

### Особенности:
<p>1) доступ в админку только для указанного в config.py id пользователя</p>
<p>2) Все обработчики событий указаны в handlers:</p>
<p>   admin.py    обработчик событий админа</p>
<p>   client.py   обработчик событий пользователя</p>
<p>3) Все запросы к бд на PostgreSQL указаны в postgres_db.py</p>
<p>4) кнопки или инлайн-кнопки указаны в keyboards</p>
<p>   admin_kb.py    кнопки админа</p>
<p>   client_kb.py   кнопки пользователя</p>
<p>5) защита от спама указана в middlewares/throttling.py</p>
<p>6) Перед деплоем на сервер, обратите внимание на polling в точке входа и замените на webhook</p>

### Как осуществляется доступ в админку:=
<p>1) создаётся закрытая группа, куда добавляется админ-пользователь и бот</p>
<p>2) Админка открывается при команде /moderator при условии если id пользователя == id админа</p>

### Пояснение config.py:
<p>1) Токен бота, выдающийся BotFather при регистрации</p>
<p>token: str = 'token' </p>
<p>2) id админа, который бот зарегистрирует в бд при первом обращении, как обычного пользователя</p>
<p>admin_ids: int = 'admin_ids'></p>
<p>3) платёжный токен, выдаваемый BotFather через разделы оплаты, либо напрямую от банка через онлайн-эквайринг</p>
<p>pay_token: str = 'pay_token'</p>
<p>4) Базовые данные входа в бд PostgreSQL:</p>
<p>    data_base_p: str = 'data_base_p'</p>
<p>    user_p: str = 'user_p'</p>
<p>    host_p: str = 'host_p'</p>
<p>    password_p: str = 'password_p'</p>
