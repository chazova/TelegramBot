import requests
import json
from config import currency

class APIException(Exception):
    pass

class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = currency[quote.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            quote_base = currency[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать {amount}')

        if quote == base:
            raise APIException('Введены одинаковые валюты')

        currency_pair = quote_ticker + quote_base
        currency_pair2 = quote_base + quote_ticker
        r = requests.get(
            f'https://currate.ru/api/?get=rates&pairs={currency_pair},{currency_pair2}&key=8361a39611175879ad94a4b6da2a4bef')
        # Пример запроса - https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key=YOUR-API-KEY
        # Пример ответа на запрос - {"status":"200","message":"rates","data":{"EURRUB":"71.3846","USDRUB":"58.059"}}
        exchange_rate = json.loads(r.content)['data'][currency_pair]
        return exchange_rate