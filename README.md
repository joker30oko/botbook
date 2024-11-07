# **Gmail Sender with Telegram**
[![Python](https://a11ybadges.com/badge?logo=python)](https://www.python.org/)
[![Telegram](https://a11ybadges.com/badge?logo=telegram)]()
[![Aiogram](https://a11ybadges.com/badge?text=Aiogram3.0&badgeColor=blue)]()

## Дисклеймер

Используя этот бот, вы соглашаетесь с тем, что будете использовать его только для законных целей. Я не несу ответственности за любые последствия, возникшие в результате использования этого скрипта, включая, но не ограничиваясь, спамом, нарушением конфиденциальности, или действиями, противоречащими политике Google. Используйте на свой страх и риск.

## Возможности бота:
1. Рассылка с нескольких аккаунтов
2. Функция генерации текста (пока что на этапе бета тестирования)
3. Возможность использования нескольких аккаунтов
4. Асинхроннная отправка сообщений
5. Тонкая настройка для рассылки
   
![image](https://github.com/user-attachments/assets/045a2a30-98c0-4cb7-898e-ff7f58199980)

6. Админ-панель

![image](https://github.com/user-attachments/assets/4025242b-4908-4215-bb48-f8c948bcb087)

7. Автоответ (пока не реализовано)
8. Онлайн отслеживание рассылок в режиме реального времени

![image](https://github.com/user-attachments/assets/7c84ea8c-4d1a-4f9b-87b0-fdc3b5e9fc60)

9. Отправка ошибок во время рассылки в отдельную группу.

## Локальный запуск бота:

**_Склонировать репозиторий к себе_**
```
git clone https://github.com/SadOnsGit/Sender-Gmail-V2.git
```
**_В директории проекта создать файл .env и заполнить своими данными:_**
```
BOT_TOKEN=''
GROUP_ID=''
```

  Где <b>BOT_TOKEN</b>, укажите токен бота полученный от @BotFather
  
  Где <b>GROUP_CHAT_ID</b>, укажите ID(айди) группы куда бот будет направлять сообщение об ошибках. <b>ВАЖНО:</b> Бот должен состоять в группе и иметь права администратора.

**_Создать и активировать виртуальное окружение:_**

Для Linux/macOS:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
Для Windows:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
**_Установить зависимости из файла requirements.txt:_**
```
pip install -r requirements.txt
```
**_Запустить бот:_**
```
python bot_run.py
```

## Запуск бота через Docker контейнер
**_Создать образ(Image) бота_**
```
docker build . -t gmailsender_bot
```
**_Создать и запустить контейнер на основе созданного образа_**
```
docker run --name senderbot gmailsender_bot
```
