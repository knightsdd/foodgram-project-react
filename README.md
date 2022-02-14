### FOODGRAM
Foodgram - сервис для просмотра и публикации рецептов

Возможности сервиса:
- Создать свой профиль
- Создавать и публиковать рецепты на основе имеющихся в базе даных ингредиентов
- Указывать теги для своих рецептов
- Загружать изображения своих рецептов
- Просматривать рецепты других пользователей
- Добавлять рецепты в избранное
- Добавлять рецепты в корзину
- Формировать список покупок (список ингредиентов с количеством) из рецептов в корзине
- Подписываться на других пользователей
- Фильтровать рецепты по тегам

### Технологии:
Бекэнд Foodgram это Django проект с реализованным API для фронтенда. API построен на Django Rest Framework (DRF). Используется базада данных PostgreSQL.


### Как запустить backend проекта локально:

Клонировать репозиторий и перейти директорию infra:

```
git clone git@github.com:knightsdd/foodgram-project-react.git

cd ./infra
```

Создайте в диреткории infra файл окружения .env, содержащий информацию о подключении к базе данных:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres # Your data_base
POSTGRES_USER=postgres # Your user
POSTGRES_PASSWORD=postgres # Your password
DB_HOST=db
DB_PORT=5432
```

Убедитесь, что у вас установлен docker и docker-compose. После чего выполните команду:

```
docker-compose up --build
```

После успешного запуска контейнеров, выполните миграции и соберите статику с помощью следующих команд:

```
docker-compose exec backend python3 manage.py migrate
```

```
docker-compose exec backend python3 manage.py collectstatic --no-input
```

При необходимости создайте суперпользователя командой:

```
docker-compose exec backend python3 manage.py createsuperuser
```

Можно воспользоваться готовыми тестовыми данными, для заполнения базы данных:

```
docker-compose exec backend python3 manage.py load_tags --path './core/data/tags.csv'
docker-compose exec backend python3 manage.py load_users --path './core/data/users.csv'
docker-compose exec backend python3 manage.py load_ingredients --path './core/data/ingredients.csv'
```

Пользователи имеют следующие учетные данные:

user01@foodgram.ru us123456
user02@foodgram.ru us123456
user03@foodgram.ru us123456
user04@foodgram.ru us123456
user05@foodgram.ru us123456
user06@foodgram.ru us123456

Учетные данные суперпользователя для демо режима:
admin@foodgram.ru aid123456

Админ панель доступна по адресу: http://localhost/admin/

Доступные endpoints можно увидеть по адресу: http://localhost/api/schema/swagger-ui/
