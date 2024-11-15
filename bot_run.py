import asyncio

from routers.user_private import router_start
from routers.admin import router_admin
from callbacks.cb_access import access_router

from callbacks.cb_start_work import router_cb_start
from callbacks.cb_cancel import cb_cancel_router
from callbacks.cb_adminpanel import cb_adminpanel

from bot_create import dp, bot
from db.create_db import init_db

# Подключение роутеров
dp.include_routers(
    router_start,
    router_cb_start,
    cb_cancel_router,
    cb_adminpanel,
    access_router,
    router_admin
)


async def main():
    """Главная функция старта бота"""
    await init_db()
    await dp.start_polling(bot)


asyncio.run(main())
