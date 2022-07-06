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


### Как запустить проект локально:

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

Админ панель доступна по адресу: http://localhost/admin/

Доступные endpoints можно увидеть по адресу: http://localhost/api/schema/swagger-ui/

### Как запустить проект на сервере:

Запуск проекта на сервере осуществляется через Github Actions. Файл foodgram_workflows.yml лежит в репозитории по адресу .github/workflows.

В нем содержаться автоматизированые инструкции для:
- тестирования кода на соответствие PEP8
- загрузки образов фронтэнда и бекэнда на dockerhub
- деплой проекта на сервер

Для успешного запуска на боевом сервере потребуется:

1. Создать следующие переменные окружения в Github Actions Secrets:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres # Название вашей базы данных
POSTGRES_USER=postgres # Имя пользователя с правами доступа для базы данных
POSTGRES_PASSWORD=postgres # Пароль для пользователя
DB_HOST=db
DB_PORT=5432
NGINX_HOST_IP=123.123.123.123 # ip адрес серевера на который деплоим проект
NGINX_HOST_NAME=mybesthost.com # Доменное имя сервера на который деплоим проект
USER=server_username # Имя пользователя на сервере
SSH_KEY=**** # ssh ключ для удаленного доступа к серверу
PASSPHRASE=******* # Пароль от ssh ключа
DOCKER_USERNAME=docker_user # Логин на dockerhub
DOCKER_PASSWORD=**** # Пароль на dockerhub
```

2. Скопировать файл docker-compose.yaml (из корня репозитория) и nginx.conf (из папки infra) в одну директорию на вашем сервере.

3. Сделать комит и пуш в ветку мастер.

```
git push
```

4. При необходимости создайте суперпользователя командой:

```
docker-compose exec backend python3 manage.py createsuperuser
```

5. Можно воспользоваться командами, для заполнения базы тестовыми данными:

```
docker-compose exec backend python3 manage.py load_tags --path './core/data/tags.csv'
docker-compose exec backend python3 manage.py load_users --path './core/data/users.csv'
docker-compose exec backend python3 manage.py load_ingredients --path './core/data/ingredients.csv'
```

Дополнительная информация:

На данный момент проект запущен по адресу:
http://knightsd.cohort3plus.ru/

Учетные данные суперпользователя для демо режима:
Имя пользователя: admin@foodgram.ru
Пароль: aid123456

