from bot_create import bot, group_id

from keyboard.mkp_access import create_access_keyboard


async def send_to_group(message: str):
    await bot.send_message(chat_id=group_id, text=message, parse_mode='html')


async def send_to_group_request(message: str, id: int):
    await bot.send_message(
        chat_id=group_id,
        text=message, 
        parse_mode='html',
        reply_markup=create_access_keyboard(id)
    )


async def send_to_user(user_id: int, message: str):
    await bot.send_message(
        chat_id=user_id,
        text=message, 
        parse_mode='html'
    )
