from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


mkp_cancel = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='❌ Отмена',
                             callback_data='cancel.actions')
    ]
])

mkp_cancel_sender = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='❌ Отменить рассылку',
                             callback_data='cancel.sender')
    ]
])