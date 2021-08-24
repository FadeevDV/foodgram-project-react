# foodgram-project-react

[![foodgram-project workflow](https://github.com/FadeevDV/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/FadeevDV/foodgram-project-react/actions/workflows/main.yml)


<p><a href="https://www.python.org/" rel="nofollow"><img src="https://camo.githubusercontent.com/938bc97e6c0351babffcd724243f78c6654833e451efc6ce3f5d66a635727a9c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d507974686f6e2d3436343634363f3f7374796c653d666c61742d737175617265266c6f676f3d507974686f6e" alt="Python" data-canonical-src="https://img.shields.io/badge/-Python-464646??style=flat-square&amp;logo=Python" style="max-width:100%;"></a>
<a href="https://www.djangoproject.com/" rel="nofollow"><img src="https://camo.githubusercontent.com/99e48bebd1b4c03828d16f8625f34439aa7d298ea573dd4e209ea593a769bd06/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d446a616e676f2d3436343634363f3f7374796c653d666c61742d737175617265266c6f676f3d446a616e676f" alt="Django" data-canonical-src="https://img.shields.io/badge/-Django-464646??style=flat-square&amp;logo=Django" style="max-width:100%;"></a>
<a href="https://www.docker.com/" rel="nofollow"><img src="https://camo.githubusercontent.com/038c45c7c5f0059723bba28b5b77bd9ac7994c8da774814c8fcb620f4bc61b35/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d646f636b65722d3436343634363f3f7374796c653d666c61742d737175617265266c6f676f3d646f636b6572" alt="docker" data-canonical-src="https://img.shields.io/badge/-docker-464646??style=flat-square&amp;logo=docker" style="max-width:100%;"></a>
<a href="https://www.postgresql.org/" rel="nofollow"><img src="https://camo.githubusercontent.com/18b5ef277b89701f948c212d45d3460070037bda9712fe5f1e64315811356ea2/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d506f737467726553514c2d3436343634363f3f7374796c653d666c61742d737175617265266c6f676f3d506f737467726553514c" alt="PostgreSQL" data-canonical-src="https://img.shields.io/badge/-PostgreSQL-464646??style=flat-square&amp;logo=PostgreSQL" style="max-width:100%;"></a>
<a href="https://www.sqlite.org/index.html" rel="nofollow"><img src="https://camo.githubusercontent.com/2c46c2b57530e634094dcb5ca341adbd8cc101300fd0968991b2a2700f1ac318/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d53514c6974652d3436343634363f3f7374796c653d666c61742d737175617265266c6f676f3d53514c697465" alt="SQLite" data-canonical-src="https://img.shields.io/badge/-SQLite-464646??style=flat-square&amp;logo=SQLite" style="max-width:100%;"></a>
<a href="https://github.com/"><img src="https://camo.githubusercontent.com/ca897bbf26e1c6429197c0c0f53e16f1625eaa99d0bc8caa4934c4b12ece45a1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d4769744875622d3436343634363f3f7374796c653d666c61742d737175617265266c6f676f3d476974487562" alt="GitHub" data-canonical-src="https://img.shields.io/badge/-GitHub-464646??style=flat-square&amp;logo=GitHub" style="max-width:100%;"></a>
<a href="https://github.com/features/actions"><img src="https://camo.githubusercontent.com/b70fe9e64e76d385b8cae9b6366dfba69af953e85d16cf43bb1f9d46fefb1621/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d476974487562253230416374696f6e732d3436343634363f3f7374796c653d666c61742d737175617265266c6f676f3d476974487562253230616374696f6e73" alt="GitHub%20Actions" data-canonical-src="https://img.shields.io/badge/-GitHub%20Actions-464646??style=flat-square&amp;logo=GitHub%20actions" style="max-width:100%;"></a>
<a href="https://nginx.org/ru/" rel="nofollow"><img src="https://camo.githubusercontent.com/b9f9edede39c7f898e25e81ce431f7c4b8d0b375c05768fd6916e599fcba219f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d4e47494e582d3436343634363f3f7374796c653d666c61742d737175617265266c6f676f3d4e47494e58" alt="NGINX" data-canonical-src="https://img.shields.io/badge/-NGINX-464646??style=flat-square&amp;logo=NGINX" style="max-width:100%;"></a></p>

## Описание
«Продуктовый помощник» (Проект Яндекс.Практикум)
Сайт является - базой кулинарных рецептов. Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в txt формате. Также присутствует файл docker-compose, позволяющий , быстро развернуть контейнер базы данных (PostgreSQL), контейнер проекта django + gunicorn и контейнер nginx

# Как запустить
Клонируем проект: 
```
git clone https://github.com/FadeevDV/foodgram-project-react.git
```
Для добавления файла .env с настройками базы данных на сервер необходимо:

Установить соединение с сервером по протоколу ssh:

  ```
  ssh username@00.000.000.00
  ```

Где username - имя пользователя, под которым будет выполнено подключение к серверу.

server_address - IP-адрес сервера или доменное имя.

Например:

  ```
  ssh praktikum@00.000.000.00
  ```

В домашней директории проекта Создать папку app/:

  ```
  mkdir app
  ```
  
В ней создать папку fodgram-project/:

  ```
  mkdir app/foodgram-project
  
  ```
В ней создать файл .env:

  ```
   sudo touch app/foodgram-project/.env
  ```


Выполнить следующую команду:

  ```
  sudo nano app/foodgram-project/.env
  ```
  
Пример добавляемых настроек:


  ```
  DB_ENGINE=django.db.backends.postgresql
  DB_NAME=postgres
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  DB_HOST=postgres
  DB_PORT=5432
  
  ```

Также необходимо добавить Action secrets в репозитории на GitHub в разделе settings -> Secrets:

* DOCKER_PASSWORD - пароль от DockerHub;
* DOCKER_USERNAME - имя пользователя на DockerHub;
* HOST - ip-адрес сервера;
* SSH_KEY - приватный ssh ключ (публичный должен быть на сервере);
* Опционно:
   ```
  * TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
  * TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)
   ```
# Проверка работоспособности
Теперь если внести любые изменения в проект и выполнить:

  ```
  git add .
  git commit -m "..."
  git push
  ```


Комманда git push является триггером workflow проекта. При выполнении команды git push запустится набор блоков комманд jobs (см. файл main.yaml). Последовательно будут выполнены следующие блоки:
  
  * tests - тестирование проекта на соответствие PEP8 и тестам pytest.

  * build_and_push_to_docker_hub - при успешном прохождении тестов собирается образ (image) для docker контейнера и отправлятеся в DockerHub

  * deploy - после отправки образа на DockerHub начинается деплой проекта на сервере. Происходит копирование следующих файлов с репозитория на сервер:
  
    ```
    1 docker-compose.yaml, необходимый для сборки трех контейнеров:
      1.1 postgres - контейнер базы данных
      1.2 web - контейнер Django приложения + wsgi-сервер gunicorn
      1.3 nginx - веб-сервер
    2 nginx/default.conf - файл кофигурации nginx сервера
    3 static - папка со статическими файлами проекта
    ```

После копировния происходит установка docker и docker-compose на сервере и начинается сборка и запуск контейнеров.

* send_message - после сборки и запуска контейнеров происходит отправка сообщения в телеграм об успешном окончании workflow

После выполнения вышеуказанных процедур необходимо установить соединение с сервером:

  ```
  ssh username@server_address
  ```

Отобразить список работающих контейнеров:

  ```
  sudo docker container ls
  ```

В списке контейнеров копировать CONTAINER ID контейнера username/yamdb_final_web:latest (username - имя пользователя на DockerHub):

  ```
  CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                NAMES
  9338873f6a9e   nginx:1.19.6           "/docker-entrypoint.…"   45 seconds ago   Up 43 seconds   0.0.0.0:80->80/tcp   foodgram-project_nginx_1
  d415a082597e   FadeevDV/foodgram:v1   "/bin/sh -c 'gunicor…"   47 seconds ago   Up 45 seconds                        foodgram-project_web_1
  d8cb992faa64   postgres:12.4          "docker-entrypoint.s…"   4 minutes ago    Up 46 seconds   5432/tcp             foodgram-project_postgres_1
  ```

Выполнить вход в контейнер:

  ```
  sudo docker exec -it d415a082597e bash
  ```

Внутри контейнера выполнить миграции:

  ```
  python manage.py migrate
  ```


Также можно наполнить базу данных начальными тестовыми данными:

  ```
  python3 manage.py shell
  >>> from django.contrib.contenttypes.models import ContentType
  >>> ContentType.objects.all().delete()
  >>> quit()
  python manage.py loaddata dump.json
  ```
Теперь проекту доступна статика. В админке Django (http://<server_address>/admin) доступно управление данными. Если загрузить фикструры, то будет доступен superuser:

```
  user: Admin
  password: admin
  email: admin@admin.com
```

Для создания нового суперпользователя можно выполнить команду:

  ```
  $ python manage.py createsuperuser
  ```
  
Для остановки и удаления контейнеров и образов на сервере:

  ```
  sudo docker stop $(sudo docker ps -a -q) && sudo docker rm $(sudo docker ps -a -q) && sudo docker rmi $(sudo docker images -q)
  ```

# Автор:


* [Дмитрий Фадеев](https://github.com/FadeevDV)
* [Сайт](http://00.00.00.00)



