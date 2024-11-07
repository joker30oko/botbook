from aiogram import Router
from aiogram.filters import Command
from aiogram import types

from keyboard.mkp_adminpanel import mkp_panel

from settings import config


router_admin = Router()

@router_admin.message(Command('admin'))
async def admin_menu(msg: types.Message):
    if msg.from_user.id in config.get_admins():
        await msg.answer('<b>💎 Админка</b>',
                        parse_mode='html', reply_markup=mkp_panel)