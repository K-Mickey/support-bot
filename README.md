# Support Bot
Боты для Telegram или VK, которых можно обучить и использовать для поддержки пользователей. 
Они смогут ответить на популярные вопросы, снизить скорость ответа и ускорить обработку сообщений. 
Для ответов на сообщения боты интегрированы с сервисом [Dialogflow](https://dialogflow.cloud.google.com/).

Примеры работы ботов: [Telegram](https://t.me/my_bubot), [группа VK](https://vk.com/club229816609)


![tg-example.gif](src/tg-example.gif)
![vk-example.gif](src/vk-example.gif)
## 📦 Установка
Проект был реализован в Python 3.13, работа в других версиях не гарантирована. 
Для начала установки необходимо скачать код проекта на компьютер.
### Установить зависимости:
Для UV:
```bash
uv venv
source .venv/bin/activate  # Linux/MacOS
# source .\.venv\Scripts\activate  # Windows
uv pip sync pyproject.toml uv.lock
```

Без UV:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
# source .\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Создать файл .env
Создайте файл .env в папке `src/` и заполните его обязательными данными:
- **TG_TOKEN** - токен бота поддержки Telegram. Создать через [@BotFather](https://t.me/BotFather)
- **VK_TOKEN** - токен бота поддержки VK. Взять в настройках своей группы
- **PROJECT_ID** - айди проекта в Google Cloud. Узнать в [консоли](https://console.cloud.google.com/)
- **GOOGLE_APPLICATION_CREDENTIALS** - путь к файлу с ключами Google Cloud. Скачать файл в [консоли](https://console.cloud.google.com/)
- **ADMIN_ID** - айди администратора в Telegram для получения логов. Узнать в [боте](https://t.me/userinfobot)
- **LOG_BOT_TOKEN** - токен бота в Telegram для отправки логов. Создать через [@BotFather](https://t.me/BotFather)

Опциональные настройки:
- **LANGUAGE_CODE** - язык общения с ботом. По умолчанию ru-RU
- **RESTART_DELAY** - задержка перезагрузки бота в секундах. По умолчанию 120
- **LOG_LEVEL** - уровень логирования. По умолчанию INFO
- **LOG_FORMAT** - формат логирования

## 🚀 Использование
Запустите ботов в терминале:
```bash
uv run tg_bot.py
uv run vk_bot.py

# python3 tg_bot.py
# python3 vk_bot.py
```

### Обучение ботов
Подготовьте JSON файл с вопросами и ответами следующего вида:
```json
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    }
}
```
Разместите файл в папке `src/` под названием `questions.json`. 
По умолчанию бот будет искать этот файл для обучения. 
В той же папке находится пример файла `questions-example.json`.
После этого запустите скрипт командой `python3 training_dialogflow.py`.
При повторном запуске обучения может возникнуть конфликт вопросов. 
В этом случае скрипт удаляет старые варианты вопроса и добавляет новые.


## 📄 Цели проекта
Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org/).