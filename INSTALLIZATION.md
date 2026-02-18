# Запуск проекта
Для просмотра, нажмите ``CTRL+SHIFT+V`` если вы на vs code
1. Нужно будет клонировать [репозиторий (кликните)](https://github.com/XZERON0/ProjectTwelve.git)  
2. Создать виртуальное окружение и позже перейдете по нему 
```pyhon
python -m venv venv
venv/scripts/activate.ps1 # window
source venv/scripts/activate #bash
```
3.  Скачать зависимости python
```python
pip install -r requirements.txt
```
4. Создайте .env и заполните значение, которые используются с библиотекой decouple 
5. Перейдите в директорию **project**
6. Запустите tailwind и сервер
```
python manage.py tailwind start
python manage.py runserver
```

## Создание установщика
1. Вводите команду в терминал (**Важно: вы должны находится в корне директории самого ``ДЖАНГО`` проекта**)
```python
pyinstall --noconsole --paths . --add-data ".env" run.py
```
2. Скачиваете ``Inno Setup``  [кликнув сюда](https://jrsoftware.org/isdl.php)
3. Билдите .iss файл и запускаете его
4. Все! Установщик проекта готов