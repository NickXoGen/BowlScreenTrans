# BowlScreenTrans

Офлайн-переводчик текста с экрана. Программа позволяет выделить любую область на экране (хоткей `Ctrl+Alt+T`), распознать там текст с помощью OCR (Tesseract) и перевести его локально через Argos Translate.

## Возможности

* Полностью офлайн-перевод (EN <-> RU).
* Работа в системном трее.
* Автоматическое сохранение скриншотов с переводом в папку `Изображения\BowlScreenTrans`.
* Журнал переводов с возможностью копирования.

## Установка (для разработчиков)

Требуется Python 3.12.

1. Клонируйте репозиторий:
   `git clone https://github.com/ВАШ_НИК/BowlScreenTrans.git`
2. Создайте виртуальное окружение:
   `python -m venv .venv`
   `.\.venv\Scripts\activate`
3. Установите зависимости:
   `pip install -r requirements.txt`
4. Установите [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (обязательно выберите русский и английский языки при установке). Укажите путь к `tesseract.exe` в файле `config.py`.
5. Запустите:
   `python main.py`

## Сборка в EXE

Сборка производится через PyInstaller с использованием файла конфигурации `build.spec`:

`pyinstaller build.spec`

Готовый файл `BowlScreenTrans.exe` появится в папке `dist`.

## Для обычных пользователей

Скачайте готовый `BowlScreenTrans.exe` в разделе [Releases](../../releases). Tesseract OCR уже встроен в сборку, устанавливать ничего не нужно. 
Внимание: из-за встроенных нейросетей (PyTorch, Stanza) файл весит около 300 МБ.