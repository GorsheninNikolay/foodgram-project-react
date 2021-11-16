# FoodGram

![foodgram-project-react_workflow](https://github.com/GorsheninNikolay/foodgram-project-react/actions/workflows/docker-image.yml/badge.svg)
![foodgram-project-react_coverage](https://github.com/GorsheninNikolay/foodgram-project-react/blob/master/backend/foodgram_backend/coverage.svg)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Данный проект представляет собой сайт "Продуктовый помощник. Моя задача состояла в написании API и упаковке проекта в Docker, а также развертывание на удаленном сервере.

Подробнее про API можно прочитать в документации после запуска проекта http://127.0.0.1/api/docs/

Функциональность
---

- Проект доступен по IP или доменному имени.

- Все сервисы и страницы доступны для пользователей в соответствии с их правами.

- Рецепты на всех страницах сортируются по дате публикации (новые — выше).

- Работает фильтрация по тегам, в том числе на странице избранного и на странице рецептов одного автора).

- Работает пагинатор (в том числе при фильтрации по тегам).

- Исходные данные предзагружены; добавлены тестовые пользователи и рецепты.

Для авторизованных пользователей:
---

- Доступна главная страница.

- Доступна страница другого пользователя.

- Доступна страница отдельного рецепта.

- Доступна страница «Мои подписки».
 
    * Можно подписаться и отписаться на странице рецепта.

    * Можно подписаться и отписаться на странице автора.

    * При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки.

    * Доступна страница «Избранное».

1. На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда.

2. На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда.

    * Доступна страница «Список покупок».

1. На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда.

2. На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда.

3. Есть возможность выгрузить файл (.txt или .pdf) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок».

4. Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента.

    * Доступна страница «Создать рецепт».

1. Есть возможность опубликовать свой рецепт.

2. Есть возможность отредактировать и сохранить изменения в своём рецепте.

3. Есть возможность удалить свой рецепт.

  * Доступна и работает форма изменения пароля.

  * Доступна возможность выйти из системы (разлогиниться).

Для неавторизованных пользователей
---

  * Доступна главная страница.

  * Доступна страница отдельного рецепта.

  * Доступна страница любого пользователя.

  * Доступна и работает форма авторизации.

  * Доступна и работает система восстановления пароля.

  * Доступна и работает форма регистрации.

Администратор и админ-зона
---

- Все модели выведены в админ-зону.

- Для модели пользователей включена фильтрация по имени и email.

- Для модели рецептов включена фильтрация по названию, автору и тегам.

- На админ-странице рецепта отображается общее число добавлений этого рецепта в избранное.

- Для модели ингредиентов включена фильтрация по названию.

- Инфраструктура

- Проект работает с СУБД PostgreSQL.

- Проект запущен на сервере в Яндекс.Облаке в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn. Заготовленный контейнер с фронтендом используется для сборки файлов.

- Контейнер с проектом обновляется на Docker Hub.

- В nginx настроена раздача статики, запросы с фронтенда переадресуются в контейнер с Gunicorn. Джанго-админка работает напрямую через Gunicorn.

- Данные сохраняются в volumes.

Оформление кода
---
Код соответствует PEP8.


# Развертывание проекта
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
