from aiogram import Router
from aiogram.filters import Command
from aiogram import types

from keyboard.mkp_main import mkp_main

from settings import config


router_start = Router()


@router_start.message(Command('start'))
async def start_message(msg: types.Message):
    if msg.from_user.id in config.get_users():
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
            f'<b>Нет доступа. Ваш айди: {msg.from_user.id}</b>',
            parse_mode='html'
        )