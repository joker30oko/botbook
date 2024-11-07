from bot_create import bot, group_id


async def send_to_group(message: str):
    await bot.send_message(chat_id=group_id, text=message, parse_mode='html')
