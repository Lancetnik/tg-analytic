# Tg-Analytic

Проект предназначен для управления инфраструктурой сбора нформации из различных Telegram-каналов,
сохранения накопленных данных и их последующего анализа.

Пользователь имеет возможность регистрировать собственные Telegram-аккаунты, от имени которых будет происходить
сбор данных, подписывать эти аккаунты на конкретные каналы и просматривать собранную информацию.

### Стек технологий
* Backend - python:Fastapi
* Fronted - VueJs2:Vuetify
* Websockets - python:Fastapi + grpcio
* Постоянные данные, необходимые для авторизации, хранятся в **Postgres**.
* В качестве хранилища собираемой информации используется **Elasticsearch**.
* Для хранения фотографий и видеозаписей используется объектное хранилище **Minio**.

## Развертывание
### Backend
1) В корне запускаем `docker-compose up es postgres redis minio`
2) В `back/app/config` изменяем `example.yml` на `config.yml` со своими данными для postgres
3) В `back/` создаем окружение `python3.9 -m venv venv` и активируем его
4) Ставим dev зависимости `python3.9 -m pip install -r dev_requirements.txt`
5) Переходим в `back/app/` и проводим миграции `./init_project.sh`
6) Запускаем приложение `uvicorn serve:app --host 0.0.0.0 --port 8000`
* Без сбилженного фронта `http://127.0.0.1:8000/` будет выдавать ошибку

### Frontend
1) Переходим во `front/`, устанавливаем зависимости `npm install`
2) Билдим фронтенд в django `npm run build`
3) Приложение билдится в директории `back/app/index/static/` и `back/app/index/templates/`
и становится доступно с backend'а по [адресу](http://127.0.0.1:8000/)

### Websockets
1) Переходим в `websockets/`, создаем окружение `python3.9 -m venv venv` и активируем его
2) Ставим зависимости `python3.9 -m pip install -r requirements.txt`
3) Переходим в `websockets/app/`, запускаем сервис `uvicorn serve:app --host 0.0.0.0 --port 8001`
* Можно запустить через `docker-compose up sockets`

### Kibana
1) Запускаем `docker-compose up kibana`
2) Идем по [адресу](http://127.0.0.1:5601)
3) Наслаждаемся доступом ко всем собранным данным в индексе `posts`

### Minio
1) Запускаем `docker-compose up kibana`
2) Идем по [адресу](http://127.0.0.1:9001/)
3) Заходим под `user` - `password`
3) Наслаждаемся доступом ко всем собранным файлам
