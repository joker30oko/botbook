from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


mkp_cancel = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='❌ Отмена',
                             callback_data='cancel.actions')
    ]
])