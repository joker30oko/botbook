from aiogram import Router
from aiogram.filters import Command
from aiogram import types

from keyboard.mkp_main import mkp_main

from settings import config
from external.messages import send_to_group_request
from db.create_db import create_user, get_user_by_telegram_id


router_start = Router()


@router_start.message(Command('start'))
async def start_message(msg: types.Message):
    existing_user = await get_user_by_telegram_id(msg.from_user.id)
    
    if existing_user:
        if existing_user.has_access:  # Проверяем поле has_access
            await msg.answer(
                '<b>Добро пожаловать в бота рассылку Гостевых.'
                '\n🛠 Текущие настройки проекта:'
                f'\n🤖 Генерация текста: {"включена" if config.get_generation() else "выключена"}'
                f'\n⏳ Задержка между сообщениями: {config.get_delay()} секунд(-ы)'
                f'\n🤖 Статус бота: {"занят ❌" if config.get_busy() else "свободен ✅"}'
                '\nИмейте в виду, что бот рассылает только гостевые букинга, остальные почты игнорируются!</b>',
                parse_mode='html',
                reply_markup=mkp_main
            )
        else:
            await msg.answer(
                '<b>❌ У вас нет доступа к этому боту.</b>',
                parse_mode='html'
            )
    else:
        # Если пользователя нет в базе данных, отправляем заявку
        await send_to_group_request(
            f'<b>✅ Новая заявка в бота\n👤 Пользователь: @{msg.from_user.username}\n🆔 Айди: {msg.from_user.id}</b>',
            msg.from_user.id
        )
        await create_user(msg.from_user.id)  # Создаем пользователя
        await msg.answer(
            '<b>✅ Заявка успешна отправлена. Ожидайте.</b>',
            parse_mode='html'
        )