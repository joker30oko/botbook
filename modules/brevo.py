import aiohttp

async def get_account_status(api_key, text=True):
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
                status_service = True
                for plan in account_info.get('plan', []):
                    if plan['creditsType'] == 'sendLimit':
                        remaining_sends = plan['credits']
                        break
                if not account_info.get('relay', {}).get('enabled', False):
                    status_service = False
                if text:
                    return f'Количество оставшихся отправок: {remaining_sends}. Статус сервера: {status_service}'
                else:
                    return status_service
            else:
                return f"Ошибка: {response.status}, {await response.text()}"
            
async 