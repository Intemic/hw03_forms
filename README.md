# Социальная сеть Yatube

Предоставляет возможность пользователям создать учетную запись, публиковать записи,
подписываться на любимых авторов и отмечать понравившиеся записи.

### Основано на Django версии 2.2.6

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git git@github.com:Intemic/hw03_forms.git
```

```
cd hw03_forms
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
