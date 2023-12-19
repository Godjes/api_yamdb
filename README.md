## Проект YaMDb

### **описание проекта*
Проект YaMDb собирает отзывы пользователей на произведения

### **Используемые технологии**


| программа                     | версия |
|-------------------------------|--------|
| Django                        | 3.2.16 |
| pytest                        | 6.2.4  |
| pytest-pythonpath             | 0.7.3  |
| pytest-django                 | 4.4.0  |
| djangorestframework           | 3.12.4 |
| djangorestframework-simplejwt | 4.7.2  |
| Pillow                        | 9.3.0  |
| PyJWT                         | 2.8.0  |
| requests                      | 2.26.0 |
| djoser                        | 2.1.0  |

### **Запускаем проект в dev режиме на OC Linux**
**Клонировать репозиторий с GitHub**
```
git clone git@github.com:boginskiy/api-Yatube.git
```

**Установить виртуальное окружение venv**
```
python3 -m venv venv
```

**Aктивировать виртуальное окружение venv**
```
source venv/bin/activate
```

**Обновить менеджер пакетов pip**
```
python3 -m pip install --upgrade pip
```

**Установить зависимости из файла requirements.txt**
```
pip install -r requirements.txt
```

**Выполнить миграции**
```
python3 manage.py migrate
```

**Запустить проект**
```
python3 manage.py runserver
```

## **API запросы**
### ***Регистрация пользователя***
Зарегестрироваться POST`http://127.0.0.1:8000/api/v1/auth/signup/`.

Получить код подтверждения на переданный email. Права доступа: Доступно без токена. Использовать имя 'me' в качестве username запрещено. Поля email и username должны быть уникальными. Должна быть возможность повторного запроса кода подтверждения.

email -required string <= 254 characters
username - required string <= 150 characters ^[\w.@+-]+\Z

### **GET запрос**
Получение списка всех произведений GET `http://127.0.0.1:8000/api/v1/titles/`.
Добавление новой публикации в коллекцию публикаций. Анонимные запросы запрещены.
```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
{
"name": "string",
"slug": "string"
}
],
"category": {
"name": "string",
"slug": "string"
}
}
]
}
```
### **GET Получение списка всех пользователей**
Получить список всех пользователей. Права доступа: Администратор GET `http://127.0.0.1:8000/api/v1/users/`.

```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
]
}
```
