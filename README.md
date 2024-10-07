# 🍉 [Foodgram](https://www.foodbananagram.hopto.org/)

### Данные для доступа к админке:
🍪 сайт: [foodbananagram.hopto.org](https://foodbananagram.hopto.org/)

🍪 email для входа в админку: admin@example.com

🍪 пароль: 123

### Описание проекта:

Foodgram - это кулинарный сайт, где пользователи могут публиковать свои рецепты,
добавлять чужие рецепты в избранное и подписываться на публикации других авторов. 

Зарегистрированным пользователям также доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Возможности проекта

- Публикация рецептов
- Добавление рецептов в избранное
- Подписка на публикации других авторов
- Создание списка продуктов для выбранных рецептов и возможность скачивания его в текстовом формате

### Стек технологий

- Python
- Django
- Django REST Framework
- Docker
- Djoser
- PostgreSQL
- Nginx
- gunicorn

### Запуск проекта:

Форкнуть и клонировать репозиторий.
```
git@github.com:frankybanana/foodgram.git
```
Создать файл с переменными окружения .env (пример доступен в проекте в файле env.example).

Установить зависимости:
```
pip install -r requirements.txt
```
Запустить Docker Compose:
```
docker compose up
```
Выполнить миграции, заполнить ингредиенты и собрать статические файлы бэкенда:
```
docker compose exec backend python manage.py migrate
```
```
docker compose exec backend python manage.py import_csv ingredients.csv
```
```
docker compose exec backend python manage.py collectstatic
```
```
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```
### Примеры запросов:

1. POST запрос к /api/users/ формата:

```
{
  "email": "cherry@yandex.ru",
  "username": "cherry",
  "first_name": "Вишня",
  "last_name": "Вишнёвая",
  "password": "yfhd3781!"
}
```
Зарегистрирует пользователя и вернет ответ формата:

```
{
  "email": "cherry@yandex.ru",
  "id": 0,
  "username": "cherry",
  "first_name": "Вишня",
  "last_name": "Вишнёвая"
}
```
2. GET запрос к /api/ingredients/{id}/ вернёт ответ с информацией о выбранном ингредиенте под указанным id:

```
{
  "id": 0,
  "name": "Вишнёвое варенье",
  "measurement_unit": "г"
}
```

### Автор:
https://github.com/frankybanana 🍌