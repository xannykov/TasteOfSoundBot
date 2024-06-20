<div align="center">
    <h1> TasteOfSoundBot
    <br>
    <img src="https://github.com/xannykov/TasteOfSoundBot/blob/main/src/header.jpg"/>
</div>

___
## Описание
**TasteOfSoundBot** — это Telegram-бот, который помогает найти исполнителя по вашему запросу. Он позволяет выводить информацию об артисте, альбоме, а также есть возможность скачать трек.
___
## Демонстрация

<img src="https://github.com/xannykov/TasteOfSoundBot/blob/main/src/demonstration.gif"/>

___
## Установка

1. Клонируйте репозиторий:

  ```sh
  git clone https://github.com/xannykov/ShakalRoflBot.git
  ```

2. Переход в директорию ShakalRoflBot:

  ```sh
  cd ShakalRoflBot
  ```

3. Создание виртуального окружения:

  ```sh
  py -m venv venv
  ```

4. Установите зависимости:

  ```sh
  pip install -r requirements.txt
  ```

5. Перейдите в *utils.py* и в строчке ```bot = telebot.TeleBot('TOKEN')``` введите свой TOKEN.

6. Запуск:
   
  ```sh
  py main.py
  ```
___

## Другое

### Данный чат-бот написан с использованием неофициального [API Яндекс Музыка](https://yandex-music.readthedocs.io/en/main/index.html#id3). Для того, чтобы понимать некоторые функции в коде, рекомендую ознакомиться с документацией.