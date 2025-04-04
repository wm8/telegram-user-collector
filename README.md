### Telegram user collector
Утилита для сбора пользователей каналов
##### Подготовка
Сначала нужно зарегистрировать приложение, от имени которого будет происходить авторизация, сделать это можно тут: https://my.telegram.org/apps \
Далее необходимо объявить несколько переменных среды:
* API_ID - id приложения 
* API_HASH - hash приложения
* DB_URL - строка psycopg вида postgresql+psycopg://{pg-user}:{pg-pass}@{pg-host}:{pg-port}/{pg-database-name}
##### Ручной запуск
```shell
python3 main.py <никнейм канала>
```
