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

bash
Копировать код
docker-compose up -d --build
4. Выполнение миграций и сбор статических файлов
После запуска контейнеров выполните миграции и соберите статику:

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

ps: Почему то ЯП не грузит нормальный README с кодом от Markdown
Сделал простой чтоб ты видел.
