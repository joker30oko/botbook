import requests

def get_remaining_sends(api_key):
    url = "https://api.brevo.com/v3/account"
    
    headers = {
        "accept": "application/json",
        "api-key": api_key  # Используем переданный API-ключ
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        account_info = response.json()
        
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
        return f"Ошибка: {response.status_code}, {response.text}"