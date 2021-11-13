![foodgram-project-react_workflow](https://github.com/GorsheninNikolay/foodgram-project-react/actions/workflows/docker-image.yml/badge.svg)
![foodgram-project-react_coverage](https://github.com/GorsheninNikolay/foodgram-project-react/blob/master/backend/foodgram_backend/coverage.svg)

ip: http://84.201.153.151

ip_admin: http://84.201.153.151/admin/

login: admin

password: 7v4-9pK-uYr-DuM

# praktikum_new_diplom


Развертывание проекта
---

1. Зайдите в GitBash, при необходимости установите
2. При помощи команд 

Перейти в каталог:
```
cd "каталог"
```
Подняться на уровень вверх:
```
cd .. 
```
:exclamation: Перейдите в нужный каталог для клонирования репозитория :exclamation:

3. Клонирование репозитория:
```
git clone https://github.com/GorsheninNikolay/foodgram_project-react
```
4. Перейти в каталог:
```
cd infra_sp2
```
5. Заплонение данных:
При помощи команды ```export token=***``` или создание файла .env, необходимо прописать следующие константные секретные переменные:
- DB_ENGINE
- DB_NAME
- POSTGRES_USER
- POSTGRES_PASSWORD
- DB_HOST
- DB_PORT
- SECRET_KEY
- ALLOWED_HOSTS
6. Запуск проекта:
```
docker-compose up -d --build
```
7. Выполнить миграции:
```
docker-compose exec web python manage.py makemigrations --noinput
docker-compose exec web python manage.py migrate --noinput
```
8. Создание superuser:
```
docker-compose exec web python manage.py createsuperuser
```
9. Сборка статики:
```
docker-compose exec web python manage.py collectstatic --no-input 
```
10. Загрузка тестовых данных:
```
docker-compose exec web python manage.py loaddata data/db.json
```

Готово! Можно заходить на сайт по ip адресу http://127.0.0.1/ :wink:

Если проект требуется остановить, нужно выполнить команду ```docker-compose down```

Системные требования
----

- Python 3.7.3
- Docker
- GitBash
- 4GB of Ram
