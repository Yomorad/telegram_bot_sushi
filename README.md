# Телеграмм бот для онлайн-магазина суши

## Stack
- Aiogram
- PostgreSQL
- Docker-compose

## Функционал
### Клиентская логика
- Изменение контактных данных клиента (имя, номер, адрес доставки, комментарии к заказу)
- Справочная информация о заведении
- Актуальные акции/скидки/новости заведения
- CRUD операции с позициями из меню в корзине 
- Оформление заказа (Выбор оплаты/способа и времени получения/количества персон)

### Админская логика
- CRUD операции с категориями/позициями меню
- Остановить/включить приём заказов/определённых позиций через бота
- Обновить актуальные данные о заведении
- Обновить баннер акций/скидок/новостей заведения
- Сделать рассылку пуш-уведомлений клиентам
- Операции с заказами клиента  
(Подтвердить доставку/оставить комментарий к заказу/посмотреть все заказы клиента/посмотреть заказ)
- Вернуться в режим пользователя


### Состав проекта
- data_base - подключение к бд, запросы в SQL
- handlers - расписаны обработчики команд для клиентской(client.py) и админской(admin.py) частей
- keyboards - кнопки или инлайн-кнопки меню
- middlewares - защита от спама с конфигами внутри
- bot_sushi.py - точка входа
- config.py - конфигурация бота
- create_bot.py - создание экземпляра бота Aiogram


### Как осуществляется доступ в админку
1. Создаётся закрытая группа, куда добавляется админ-пользователь и бот
2. Админка открывается при команде /moderator при условии если id пользователя равен id админа    
(указывается в настройках)

## Как развернуть проект:
### 1 Клонируем проект

```bash
git clone https://github.com/Yomorad/telegram_bot_sushi
```

### 2 Прописываем свои конфиги в .env

```bash
# Токен бота, выдающийся от BotFather боту при регистрации
TELEGRAM_BOT_TOKEN = '' - 
# ID админа(пользователя телеграмм),
# как пример его можно получить при команде /start, которая зарегистрирует в бд клиента при первом обращении с его id в чате
ADMIN_ID = ''
# платёжный токен, выдаваемый BotFather через разделы оплаты, либо напрямую от банка через онлайн-эквайринг
PAY_TOKEN = ''
# Можно также изменить параметры входа в бд, но они учитываются лишь как контейнер
```

### 3 Поднимаем контейнеры

```bash
docker compose up --build
# подключаемся к бд, как пример:
docker exec -it sushi_bot-db_service-1 psql -U postgres -d postgres
# выключаем контейнеры и удаляем привязанные тома
docker compose down -v
```