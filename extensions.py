from config import keys, api_key, token
import requests
import json

class MoneyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount:str):
        if quote == base:
            raise ConversionException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key={api_key}')
        base_amount = json.loads(r.content)['data'][f'{keys[quote]}{keys[base]}']
        total_amount = float(base_amount) * float(amount)
        return total_amount


class ConversionException(Exception):
    pass