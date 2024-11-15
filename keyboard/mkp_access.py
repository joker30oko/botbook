from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_access_keyboard(telegram_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='✅ Принять', callback_data=f'access.accept.{telegram_id}'),
            InlineKeyboardButton(text='❌ Отклонить', callback_data=f'access.reject.{telegram_id}')
        ]
    ])
