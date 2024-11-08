from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


mkp_panel = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='⌛️ Установить задержку между сообщениями',
                             callback_data='admin.setdelay')
    ],
    [
        InlineKeyboardButton(text='⌛️ Установить количество сообщений на 1 аккаунт',
                             callback_data='admin.setcount')
    ],
    [
        InlineKeyboardButton(text='🤖 Генерация текста',
                             callback_data='admin.generation')
    ],
    [
        InlineKeyboardButton(text='👤 Назначить администратора ',
                             callback_data='admin.setadmin')
    ],
    [
        InlineKeyboardButton(text='👤 Дать доступ пользователю ',
                             callback_data='admin.setuser')
    ],
    [
        InlineKeyboardButton(text='👤 Узнать количество оставшихся отправок ',
                             callback_data='admin.getcredits')
    ]
])
