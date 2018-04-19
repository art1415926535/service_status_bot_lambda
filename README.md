Для запуска необходимо:
  * python >= 3.6
  * `pip3 install -r requirements.txt`
  * Создать файл `settings.py`
  * Создать файл `urls.txt`
  * Запустить скрипт `python3.6 main.py`

Для запуска через Docker необходимо:
  * Создать файл `settings.py`
  * Создать файл `urls.txt`
  * Запустить контейнер ``


#### settings.py
```python
TOKEN = '95123483458:AAAz65W9-bghuiacsYUnbghuiMNjkMhuio'  # Токен бота.
CHAT_ID = -1000000000000  # ID чата для вывода статистики.
DEBUG = False  # Включение и выключения дебаг режима.
```

#### urls.txt
```
http://some_url.com
https://some_url.com
```
