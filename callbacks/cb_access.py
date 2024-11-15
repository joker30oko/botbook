from aiogram.types import CallbackQuery
from aiogram import Router, F

from db.create_db import update_access
from external.messages import send_to_user


access_router = Router()

@access_router.callback_query(F.data.startswith('access.'))
async def access(call: CallbackQuery):
    # Извлекаем telegram_id из callback_data
    action, decision, telegram_id = call.data.split('.')
    telegram_id = int(telegram_id)  # Преобразуем в int
    cur_text = call.message.text

    if decision == 'accept':
        # Обновляем доступ пользователя
        await update_access(telegram_id, True)  # Устанавливаем доступ
        await call.answer("✅ Доступ предоставлен!")  # Ответ пользователю
        await call.message.edit_text(
            f"<b>{cur_text} \n\n✅ Пользователь был успешно принят</b>",
            parse_mode='html'
        )
        await send_to_user(
            telegram_id,
            '<b>✅ Ваша заявка была принята, для работы с ботом введите /start</b>'
        )
    elif decision == 'reject':
        # Обновляем доступ пользователя
        await call.answer("❌ Доступ отклонен!")  # Ответ пользователю
        await call.message.edit_text(
            f"<b>{cur_text} \n\n❌ Пользователь был успешно отклонён</b>",
            parse_mode='html'
        )
        await send_to_user(
            telegram_id,
            '<b>❌ Ваша заявка была отклонена</b>'
        )
