import asyncio

from routers.user_private import router_start
from routers.admin import router_admin

from callbacks.cb_start_work import router_cb_start
from callbacks.cb_cancel import cb_cancel_router
from callbacks.cb_adminpanel import cb_adminpanel

from bot_create import dp, bot

# Подключение роутеров
dp.include_routers(
    router_start,
    router_cb_start,
    cb_cancel_router,
    cb_adminpanel,
    router_admin
)


async def main():
    """Главная функция старта бота"""
    await dp.start_polling(bot)


asyncio.run(main())
