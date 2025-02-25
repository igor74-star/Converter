import requests
from config import API_KEY

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base}/{quote}/{amount}"
        response = requests.get(url)


        print(response.status_code)
        print(response.json())

        if response.status_code != 200:
            raise APIException(f"Ошибка получения данных с API: {response.text}")

        data = response.json()
        if data['result'] != 'success':
            raise APIException(data['error-type'])

        return round(data['conversion_rate'] * amount, 2)