# Yucut - сервис для укорачивания ссылок.
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-framewfork-%23000000)](https://flask.palletsprojects.com/en/2.2.x/)

Сервис изпользуется для укорачивания длинных ссылок. Длинные ссылки записываются в базу данных с помощью SQLAlchemy, а пользователь получает в ответ укороченную ссылку.




Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Запустить приложение:

```
flask run
```
