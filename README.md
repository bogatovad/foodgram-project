# Статус Workflow
![example workflow](https://github.com/bogatovad/foodgram-project/actions/workflows/foodgram_workflow.yml/badge.svg)
### foodgram-project
http://178.154.197.184
### Админка для базы данных
http://178.154.197.184/admin/
### Описание
Продуктовый помощник.
Есть возможность создать и опубликовать свой рецепт,
подписаться на интересного автора, дабвлять рецепты в избранное,
скачивать список ингридиентов для покупки и приготовления рецептов.
### Технологии
1. Python3
2. Django REST Framework
3. Docker
4. Postgesql
5. Nginx
6. CI\CD
### Установка docker
Установите Docker в свою систему следуя инструкциям документации
https://docs.docker.com/get-docker/
### Клонирование репозитория
Затем склонируйте репозиторий к себе на компьютер, выполнив команду
```git clone https://github.com/bogatovad/foodgram-project.git```
### Команды для запуска приложения
```docker-compose up```
### Команду для создания суперпользователя
```docker-compose exec webservice python manage.py createsuperuser```
#### Команда для выполнения миграций
```docker-compose exec webservice python manage.py migrate --noinput```
### Команда для сбора статики в одну папку
```docker-compose exec webservice python manage.py collectstatic --no-input```
### Автор
Артем Богатов
