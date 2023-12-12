# Телеграм-Бот для Мониторинга Статуса Домашних Заданий
Этот бот предназначен для отслеживания статуса проверки ваших домашних заданий на Яндекс Практикуме и уведомляет вас в Telegram о результатах.

### Установка
Склонируйте репозиторий:
```
git clone git@github.com:pa2ha/homework_bot.git
```
```
 cd homework_bot
```
Создайте виртуальное окружение (рекомендуется):
 ```
 python -m venv venv
```

### Активируйте виртуальное окружение:

### Для Windows:
```
venv\Scripts\activate
```

### Для macOS/Linux:
```
source venv/bin/activate
```
### Установите зависимости:
```
pip install -r requirements.txt
```
Создайте файл .env в корне проекта и добавьте необходимые переменные окружения:
dotenv
```
PRACTICUM_TOKEN=ваш_токен_практикума
TELEGRAM_TOKEN=ваш_токен_telegram
TELEGRAM_CHAT_ID=ваш_chat_id_telegram
```
### Запустите бота:
```
python homework_bot.py
```
Теперь ваш бот запущен и готов следить за статусом ваших домашних заданий!

## Важно
Убедитесь, что у вас установлен Python версии 3.x.

Токен Практикума можно получить в вашем личном кабинете.

Токен и chat_id для Telegram получите, создав бота в BotFather.

Добавьте бота в ваш чат, чтобы получать уведомления.
