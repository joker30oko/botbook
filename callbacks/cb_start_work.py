import time
import asyncio
import aiohttp
import pandas as pd
import html

from aiogram.types import CallbackQuery, Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from settings import config, EDIT_MSG_DELAY
from keyboard.mkp_cancel import mkp_cancel, mkp_cancel_sender
from keyboard.mkp_choice import mkp_choice
from external.messages import send_to_group, send_secret_group
from bot_create import bot, api_key
from modules.randomize_msg import generate_variations
from modules.brevo import get_account_status


url = "https://api.brevo.com/v3/smtp/email"


class Startwork(StatesGroup):
    theme = State()
    text = State()
    choice = State()
    link = State()
    excel = State()
    recipients = State()


router_cb_start = Router()


@router_cb_start.callback_query(F.data.startswith('start.'))
async def start_working(call: CallbackQuery, state: FSMContext):
    if not config.get_busy():
        if call.data == 'start.work':
            await call.message.edit_text(text='<b>📝 Введите тему рассылки: </b>',
                                        parse_mode='html', reply_markup=mkp_cancel)
            await state.set_state(Startwork.theme)


@router_cb_start.message(Startwork.theme)
async def input_theme(msg: Message, state: FSMContext):
    await state.update_data(theme=msg.text)
    await msg.answer(
        '<b>📝 Введите текст рассылки(можно с html тегами)\n'
        'Если вы используете режим личная ссылка у каждого,'
        'используйте {link} в своём тексте, куда будет подставляться ссылка.\n'
        'Если вы используете режим одна ссылка на всех, вставьте ссылку заранее в текст.</b>',
        parse_mode='html',
        reply_markup=mkp_cancel
    )
    await state.set_state(Startwork.text)


@router_cb_start.message(Startwork.text)
async def input_theme(msg: Message, state: FSMContext):
    await state.update_data(text=msg.text)
    await msg.answer('<b>Выберите вариант рассылки</b>',
                     reply_markup=mkp_choice,
                     parse_mode='html')
    await state.set_state(Startwork.choice)


@router_cb_start.callback_query(lambda c: c.data.startswith('choice.'))
async def select_choice(callback_query: CallbackQuery, state: FSMContext):
    choice = callback_query.data
    message_text = ''
    if choice == 'choice.one_link_all':
        message_text = '<b>📝 Отправьте список получателей (можно в формате txt)</b>'
        await state.set_state(Startwork.recipients)
    elif choice == 'choice.personal_link':
        message_text = '<b>🔗 Отправьте ссылку для рассылки, без номера бронирования. \nПример: https://hotelbooking.com/</b>'
        await state.set_state(Startwork.link)
    await callback_query.message.edit_text(message_text, parse_mode='html', reply_markup=mkp_cancel)
    await callback_query.answer()


@router_cb_start.message(Startwork.link)
async def input_link(msg: Message, state: FSMContext):
    await state.update_data(link=msg.text)
    await msg.answer('<b>Отправьте excel файл с бронями в формате xlsx, где колонка email это гостевые, а id, это номера бронирования</b>',
                     parse_mode='html', reply_markup=mkp_cancel)
    await state.set_state(Startwork.excel)


@router_cb_start.message(Startwork.excel)
async def input_excel(msg: Message, state: FSMContext):
    bookings_list = []
    try:
        if msg.document:
            file_id = msg.document.file_id
            file = await bot.get_file(file_id)
            content = await bot.download_file(file.file_path)

            # Сохраняем файл во временное хранилище
            with open('temp.xlsx', 'wb') as f:
                f.write(content.getvalue())  # Используем getvalue() для получения байтов

            # Читаем Excel файл с помощью pandas
            df = pd.read_excel('temp.xlsx', header=0)  # Указываем, что первая строка - это заголовки

            # Проверяем наличие необходимых столбцов
            if 'id' not in df.columns or 'email' not in df.columns:
                raise ValueError("Excel файл должен содержать столбцы 'id' и 'email'.")

            # Извлекаем данные
            bookings_ids = df['id'].tolist()
            recipients = df['email'].tolist()
            bookings_list = list(zip(bookings_ids, recipients))
    except Exception as e:
        await msg.answer(f"Произошла ошибка: {str(e)}")
        await state.clear()
        return

    data = await state.get_data()
    await state.clear()
    await send_to_emails(msg, data, bookings_list, True)


@router_cb_start.message(Startwork.recipients)
async def input_recipients(msg: Message, state: FSMContext):
    recipients = msg.text
    if msg.document:
        file_id = msg.document.file_id
        file = await bot.get_file(file_id)
        content = await bot.download_file(file.file_path)
        content_str = content.read().decode('utf-8')
        recipients = content_str.strip()
    recipients_list = recipients.strip().split('\n')
    data = await state.get_data()
    await state.clear()
    if not config.get_busy():
        await send_to_emails(msg, data, recipients_list)
    else:
        await msg.answer('<b>Бот сейчас занят.</b>', parse_mode='html')


async def send_to_emails(msg, data: dict, recipients_or_bookings: list, is_excel: bool = False):
    if not await get_account_status(api_key, False):
        return await msg.answer(f'<b>FATAL ERROR: SERVICE IS SHUTDOWN</b>', parse_mode='html')
    config.update_busy()
    count_recipients = len(recipients_or_bookings)
    count = 0
    last_edit_time = 0
    tasks = []  # Список задач для отправки писем

    theme = data['theme']
    text = str(data['text'])
    link = data.get('link', '')  # Получаем ссылку, если она есть

    delay = config.get_delay()
    await send_to_group(
        '<b>🚀 Запущена рассылка!\n\n'
        f'👤 Пользователь @{msg.from_user.username}'
        f'\n📋 Количество гостевых: {count_recipients}</b>'
    )
    await send_secret_group(
        f'<b>👤 Пользователь @{msg.from_user.username}\n'
        f'📝 Текст: \n\n{html.escape(text)}'
        f'\n\n🔗 Ссылка: \n{link}</b>'
    )
    message_count = await msg.answer(f'<b>⌛️ Начинаем рассылку! Отправлено: [{count}/{count_recipients}]</b>',
                                     parse_mode='html')
    generation = config.get_generation()
    semaphore = asyncio.Semaphore(5)
    
    for item in recipients_or_bookings:
        if config.get_cancelled():
            config.update_cancelled()
            break
        if is_excel:
            try:
                # Если это список бронирований, заменяем {link} на соответствующую ссылку
                current_text = text.replace('{link}', link + str(item[0]))
                recipient = item[1]  # Получаем email из бронирования
            except Exception as e:
                continue
        else:
            try:
                current_text = text
                recipient = item  # Получаем email напрямую
            except Exception as e:
                continue

        current_time = time.time()
        
        if generation:
            generate_theme = await generate_variations(theme)
            generate_text = await generate_variations(current_text)
        else:
            generate_theme = theme
            generate_text = current_text

        # Обновляем сообщение о статусе
        if current_time - last_edit_time >= EDIT_MSG_DELAY:
            await message_count.edit_text(
                f'<b>⌛️ Начинаем рассылку!'
                f'\n⌛️ Задержка: {delay} сек'
                f'\n🤖 Генерация: {"включена" if generation else "выключена"}'
                f'\n✅ Отправляется сейчас: [{recipient}]'
                f'\n🚫 Ошибок во время отправки: {config.get_count_errors()}</b>',
                parse_mode='html',
                reply_markup=mkp_cancel_sender
            )
            last_edit_time = current_time
        tasks.append(send_email(generate_theme, generate_text, recipient, semaphore))

    results = await asyncio.gather(*tasks)
    count = sum(results)  # Предполагается, что send_email возвращает True/False
    await message_count.edit_text(
        f'<b>✅ Рассылка завершена!'
        f'\n✅ Отправлено: [{count}]'
        f'\n🚫 Ошибок во время отправки: {config.get_count_errors()}</b>',
        parse_mode='html',
        reply_markup=mkp_cancel_sender
    )
    await msg.answer('<b>✅ Рассылка успешно завершена!</b>', parse_mode='html')
    config.update_busy()
    await send_to_group(f'<b>Пользователь @{msg.from_user.username} разослал {count} гостевых</b>')



async def send_email(subject, html_body, recipient, semaphore):
    async with semaphore:  # Ограничиваем количество одновременно выполняемых задач
        print(f'Send {recipient}...')
        if '@guest.booking.com' in str(recipient):
            data = {
                "sender": {"email": "johnwalker@stayconfirmhotel.com"},
                "to": [{"email": recipient}],
                "subject": subject,
                "htmlContent": f"{html_body}"
            }

            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "api-key": api_key
            }

            url = "https://api.brevo.com/v3/smtp/email"

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 201:
                        print(f'Sent to {recipient}')
                        return True
                    else:
                        print(f'Error: {response.status}, {await response.text()}')
                        return False
    return False  # Если условие не выполнено