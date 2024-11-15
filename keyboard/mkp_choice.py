from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


mkp_choice = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Одна ссылка на всех',
                             callback_data='choice.one_link_all')
    ],
    [
        InlineKeyboardButton(text='Личная ссылка у каждого',
                             callback_data='choice.personal_link')
    ],
    [
        InlineKeyboardButton(text='Одна ссылка с вводом номера бронирования',
                             callback_data='choice.number_booking')
    ]
])
