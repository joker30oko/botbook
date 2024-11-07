from aiogram import Router
from aiogram.filters import Command
from aiogram import types

from keyboard.mkp_adminpanel import mkp_panel

from settings import config
from bot_create import api_key
from modules.brevo import get_remaining_sends


router_admin = Router()

@router_admin.message(Command('admin'))
async def admin_menu(msg: types.Message):
    if msg.from_user.id in config.get_admins():
        await msg.answer(
            '<b>💎 Админка'
            f'\nОставшиеся отправки: {get_remaining_sends(api_key)}</b>',
            parse_mode='html', reply_markup=mkp_panel
        )
