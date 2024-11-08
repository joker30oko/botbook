from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup

from bot_create import api_key
from modules.brevo import get_remaining_sends
from settings import config

class SetDelay(StatesGroup):
    setdelay = State()

class SetAdmin(StatesGroup):
    setadmin = State()
    
class SetUser(StatesGroup):
    setuser = State()

class SetCountMsg(StatesGroup):
    setcount = State()

cb_adminpanel = Router()

@cb_adminpanel.callback_query(F.data.startswith('admin.'))
async def admin_panel(call: CallbackQuery, state: FSMContext):
    if call.data == 'admin.setdelay':
        delay = config.get_delay()
        await call.message.edit_text(f'<b>Текущая задержка: {delay}\n✅ Введите новую задержку между сообщениями: </b>', parse_mode='html')
        await state.set_state(SetDelay.setdelay)
    elif call.data == 'admin.setadmin':
        await call.message.edit_text(f'<b>✅ Введите айди нового администратора: </b>', parse_mode='html')
        await state.set_state(SetAdmin.setadmin)
    elif call.data == 'admin.setuser':
        await call.message.edit_text(f'<b>✅ Введите айди нового пользователя: </b>', parse_mode='html')
        await state.set_state(SetUser.setuser)
    elif call.data == 'admin.setcount':
        count_messages = config.get_count_messages()
        await call.message.edit_text(f'<b>Текущее количество на 1 аккаунт: {count_messages}'
                                     '\n✅ Введите количество сообщений на 1 аккаунт: </b>', parse_mode='html')
        await state.set_state(SetCountMsg.setcount)
    elif call.data == 'admin.generation':
        if config.get_generation:
            config.update_generation()
            await call.message.edit_text(f'<b>🤖 Вы успешно {"включили" if config.get_generation() else "отключили"} генерацию</b>', parse_mode='html')
    elif call.data == 'admin.getcredits':
        await call.message.edit_text(
            f'<b>Оставшиеся отправки: {await get_remaining_sends(api_key)}</b>',
            parse_mode='html'
        )
    
@cb_adminpanel.message(SetDelay.setdelay)
async def setdelay(message: Message, state: FSMContext):
    try:
        delay = int(message.text)
    except ValueError:
        await message.reply("❌ Пожалуйста, введите корректное целое число.")
        return
    config.update_delay(delay)
    await message.answer(f'<b>✅ Вы успешно установили задержку в {delay} секунд.</b>', parse_mode='html')
    await state.clear()
    

@cb_adminpanel.message(SetAdmin.setadmin)
async def setadmin(message: Message, state: FSMContext):
    try:
        admin = int(message.text)
    except ValueError:
        await message.reply("❌ Пожалуйста, введите корректное целое число.")
        return
    config.set_admin(admin)
    await message.answer(f'<b>✅ Вы успешно добавили нового админа {admin}.</b>', parse_mode='html')
    await state.clear()


@cb_adminpanel.message(SetUser.setuser)
async def setuser(message: Message, state: FSMContext):
    try:
        user = int(message.text)
    except ValueError:
        await message.reply("❌ Пожалуйста, введите корректное целое число.")
        return
    config.set_user(user)
    await message.answer(f'<b>✅ Вы успешно добавили нового пользователя {user}.</b>', parse_mode='html')
    await state.clear()


@cb_adminpanel.message(SetCountMsg.setcount)
async def set_count_msg(message: Message, state: FSMContext):
    try:
        count = int(message.text)
    except ValueError:
        await message.reply("❌ Пожалуйста, введите корректное целое число.")
        return
    config.update_count_messages(count)
    await message.answer(f'<b>✅ Вы успешно установили количество сообщений на 1 аккаунт {count}.</b>', parse_mode='html')
    await state.clear()
