from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Router, F

from settings import config

cb_cancel_router = Router()


@cb_cancel_router.callback_query(F.data.startswith('cancel.'))
async def cancel_all(call: CallbackQuery, state: FSMContext):
    if call.data == 'cancel.actions':
        await call.message.edit_text('<b>❌ Успешно отменено</b>', parse_mode='html')
        await state.clear()
    elif call.data == 'cancel.sender':
        cur_text = call.message.text
        config.update_cancelled()
        await call.message.edit_text(
            f'<b>{cur_text}\n\n❌ Рассылка отменена</b>',
            parse_mode='html'
        )
