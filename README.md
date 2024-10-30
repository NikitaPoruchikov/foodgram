<<<<<<< HEAD
### Проект Foodgram

**Foodgram** — это онлайн-сервис для публикации рецептов. Пользователи могут создавать рецепты, добавлять их в избранное, подписываться на других авторов, а также формировать список покупок для удобного планирования блюд.

Для удобства навигации по сайту рецепты размечены тэгами (**Tags**)

### Технологии

![Python](https://img.shields.io/badge/Python-3.9-3670A0?style=for-the-badge&logo=python&logoColor=yellow&labelColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=black)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white&labelColor=black)
![Gunicorn](https://img.shields.io/badge/Gunicorn-298729?style=for-the-badge&logo=gunicorn&logoColor=white&labelColor=black)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white&labelColor=black)
![DjangoREST](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white&labelColor=black)




### Инструкция для разворачивания проекта на удаленном сервере:

- Склонируйте проект из репозитория:

```sh
$ git clone https://github.com/NikitaPoruchikov/foodgram.git
```

- Выполните вход на удаленный сервер

- Установите DOCKER на сервер:
```sh
apt install docker.io 
```

- Установитe docker-compose на сервер:
```sh
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

- Отредактируйте конфигурацию сервера NGNIX:
```sh
Локально измените файл ..infra/nginx.conf - замените данные в строке server_name на IP-адрес удаленного сервера
```

- Скопируйте файлы docker-compose.yml и nginx.conf из директории ../infra/ на удаленный сервер:
```sh
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yaml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
- Создайте переменные окружения (указаны в файле ../infra/env.example) и добавьте их в Secrets GitHub Actions

- Установите и активируйте виртуальное окружение (для Windows):

```sh
python -m venv venv 
source venv/Scripts/activate
python -m pip install --upgrade pip
``` 

- Запустите приложение в контейнерах:

```sh
docker-compose up -d --build
```

- Выполните миграции:

```sh
docker-compose exec backend python manage.py migrate
```

- Создайте суперпользователя:

```sh
docker-compose exec backend python manage.py createsuperuser
```

- Выполните команду для сбора статики:

```sh
docker-compose exec backend python manage.py collectstatic --no-input
```

- Команда для заполнения тестовыми данными:
```sh
docker-compose exec backend python manage.py load_ingredients
docker compose exec backend python manage.py import_tags
```

- Команда для остановки приложения в контейнерах:

```sh
docker-compose down -v
```

### Для запуска на локальной машине:

- Склонируйте проект из репозитория:

```sh
$ git clone https://github.com/NikitaPoruchikov/foodgram.git
```

- В папке ../infra/ переименуйте файл example.env в .env и заполните своими данными:
```
POSTGRES_DB=<database_name>
POSTGRES_USER=<database_user>
POSTGRES_PASSWORD=<database_password>
=======
# Foodgram - Продуктовый помощник 🍲
Foodgram — это веб-приложение, которое позволяет пользователям делиться рецептами, добавлять рецепты в избранное, подписываться на любимых авторов и формировать список покупок.

Функциональные возможности
Регистрация и авторизация: Поддержка аутентификации по токену.
Рецепты: Создание, просмотр, редактирование и удаление рецептов.
Подписки: Подписка на любимых авторов для получения обновлений.
Избранное: Добавление рецептов в список избранных.
Список покупок: Формирование и скачивание списка покупок для выбранных рецептов.
Технологии
Backend: Python 3, Django, Django REST Framework
Frontend: React
База данных: PostgreSQL
Докеризация: Docker, Docker Compose
Тестирование: Pytest, Unittest
CI/CD: GitHub Actions
Установка и запуск
1. Клонирование репозитория
git clone https://github.com/your-username/foodgram-project.git
cd foodgram-project
2. Заполнение .env файла
Создайте файл .env в корневой директории и добавьте в него следующие переменные:
DB_ENGINE=django.db.backends.postgresql
DB_NAME=имя_вашей_базы_данных
POSTGRES_USER=имя_пользователя
POSTGRES_PASSWORD=пароль
>>>>>>> 94582254688452ba7054dd99ff91c162d0d948b4
DB_HOST=db
DB_PORT=5432
SECRET_KEY=секретный_ключ_django
DEBUG=True
ALLOWED_HOSTS=*
3. Сборка и запуск контейнеров
Для запуска приложения используйте Docker Compose:
docker-compose up -d --build
4. Выполнение миграций и сбор статических файлов
После запуска контейнеров выполните миграции и соберите статику:
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
5. Создание суперпользователя
Для доступа к админке создайте суперпользователя:
docker-compose exec backend python manage.py createsuperuser

Вот пример README для проекта Foodgram с описанием функциональности, установкой и инструкциями для запуска:

Foodgram - Продуктовый помощник 🍲
Foodgram — это веб-приложение, которое позволяет пользователям делиться рецептами, добавлять рецепты в избранное, подписываться на любимых авторов и формировать список покупок.

<<<<<<< HEAD
### Особенности заполнения данными:
=======
Функциональные возможности
Регистрация и авторизация: Поддержка аутентификации по токену.
Рецепты: Создание, просмотр, редактирование и удаление рецептов.
Подписки: Подписка на любимых авторов для получения обновлений.
Избранное: Добавление рецептов в список избранных.
Список покупок: Формирование и скачивание списка покупок для выбранных рецептов.
Технологии
Backend: Python 3, Django, Django REST Framework
Frontend: React
База данных: PostgreSQL
Докеризация: Docker, Docker Compose
Тестирование: Pytest, Unittest
CI/CD: GitHub Actions
Установка и запуск
1. Клонирование репозитория
bash
Копировать код
git clone https://github.com/your-username/foodgram-project.git
cd foodgram-project
2. Заполнение .env файла
Создайте файл .env в корневой директории и добавьте в него следующие переменные:
>>>>>>> 94582254688452ba7054dd99ff91c162d0d948b4

env
Копировать код
DB_ENGINE=django.db.backends.postgresql
DB_NAME=имя_вашей_базы_данных
POSTGRES_USER=имя_пользователя
POSTGRES_PASSWORD=пароль
DB_HOST=db
DB_PORT=5432

SECRET_KEY=секретный_ключ_django
DEBUG=True
ALLOWED_HOSTS=*
3. Сборка и запуск контейнеров
Для запуска приложения используйте Docker Compose:

<<<<<<< HEAD
# Ресурсы API Foodgram
=======
bash
Копировать код
docker-compose up -d --build
4. Выполнение миграций и сбор статических файлов
После запуска контейнеров выполните миграции и соберите статику:
>>>>>>> 94582254688452ba7054dd99ff91c162d0d948b4

bash
Копировать код
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
5. Создание суперпользователя
Для доступа к админке создайте суперпользователя:

bash
Копировать код
docker-compose exec backend python manage.py createsuperuser
6. Доступ к приложению
Приложение будет доступно по адресу http://localhost.

## Использование API
Документация API
Полная документация API доступна по адресу http://localhost/api/docs/.

Примеры основных запросов

Получение списка рецептов:
GET /api/recipes/

Добавление рецепта в избранное:
POST /api/recipes/{id}/favorite/

Создание списка покупок:
GET /api/recipes/download_shopping_cart/


### Автор
Никита Поручиков 

<<<<<<< HEAD
```sh
[
    {
        "id": 1,
        "name": "абрикосовое варенье",
        "measurement_unit": "г"
    },
    ...
        {
        "id": 6,
        "name": "абрикосы консервированные",
        "measurement_unit": "г"
    }
]
```

#### Пример POST-запроса:
```
POST /api/recipes/
```
Авторизация по токену.
Запрос от имени пользователя должен выполняться с заголовком "Authorization: Token TOKENVALUE"

```sh
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

#### Пример ответа:
- код ответа сервера: 201
- тело ответа:

```sh
{
"id": 0,
"tags": [
{}
],
"author": {
"email": "user@example.com",
"id": 0,
"username": "string",
"first_name": "Вася",
"last_name": "Пупкин",
"is_subscribed": false
},
"ingredients": [
{
"id": 0,
"name": "Картофель отварной",
"measurement_unit": "г",
"amount": 1
}
],
"is_favorited": true,
"is_in_shopping_cart": true,
"name": "string",
"image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
"text": "string",
"cooking_time": 1
}
```

После запуска проект будут доступен по адресу: [http://localhost/](http://localhost/)

Документация будет доступна по адресу: [http://localhost/api/docs/](http://localhost/api/docs/)

***

Проект развернут по https://foodgrami.zapto.org/

Доступ в админ-панель:

```sh
https://foodgrami.zapto.org/admin
login: rev20240@gmail.com
pass: asd123
```

### Автор

Nikita Poruchikov
=======
ps: Почему то ЯП не грузит нормальный README с кодом от Markdown
Сделал простой чтоб ты видел.
>>>>>>> 94582254688452ba7054dd99ff91c162d0d948b4
