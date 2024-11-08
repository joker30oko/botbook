import aiohttp

async def get_remaining_sends(api_key):
    url = "https://api.brevo.com/v3/account"
    
    headers = {
        "accept": "application/json",
        "api-key": api_key  # Используем переданный API-ключ
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                account_info = await response.json()
                
                # Получите количество оставшихся отправок
                remaining_sends = None
                for plan in account_info.get('plan', []):
                    if plan['creditsType'] == 'sendLimit':
                        remaining_sends = plan['credits']
                        break
                
                if remaining_sends is not None:
                    return remaining_sends
                else:
                    return "Не удалось найти оставшиеся отправки."
            else:
                return f"Ошибка: {response.status}, {await response.text()}"