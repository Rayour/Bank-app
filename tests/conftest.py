import datetime
from typing import Any

import pandas as pd
import pytest


@pytest.fixture
def hours(request: Any) -> Any:
    """Содержит набор тестовых данных для тестирования функции src.utils.get_greeting"""

    tests = [
        {"input": "00", "output": "Доброй ночи"},
        {"input": "06", "output": "Доброе утро"},
        {"input": "12", "output": "Добрый день"},
        {"input": "18", "output": "Добрый вечер"},
    ]
    return tests[request.param]


@pytest.fixture
def df_date_operations(request: Any) -> Any:
    """Данные для тестирования функции src.utils.get_df_by_dates"""

    date1 = datetime.datetime.strptime("2025-12-01", "%Y-%m-%d")
    date2 = datetime.datetime.strptime("2025-12-02", "%Y-%m-%d")

    tests = [
        {
            "input": (pd.DataFrame({
                "Дата платежа": [date1, date2],
                "Сумма платежа": [-100.0, 100.0],
                "Номер карты": ["*1111", "*2222"],
                "Кэшбэк": [1.0, 0.0]
            }), "2025-12-01"),
            "output": {
                "Дата платежа": {0: date1},
                "Сумма платежа": {0: -100.0},
                "Номер карты": {0: '*1111'},
                "Кэшбэк": {0: 1.0}
            }
        }
    ]
    return tests[request.param]


@pytest.fixture
def df_operations(request: Any) -> Any:
    """Данные для тестирования функции src.utils.get_cards_total_info"""

    tests = [
        {
            "input": pd.DataFrame({
                "Статус": ["OK", "OK", "OK", "FAILED"],
                "Сумма платежа": [-100.0, -100.0, 100.0, -100.0],
                "Номер карты": ["*1111", "*2222", "*1111", "*2222"],
                "Кэшбэк": [1.0, 0.0, 1.0, 1.0]
            }),
            "output": [
                {
                    "last_digits": "1111",
                    "total_spent": 100.0,
                    "cashback": 1.0
                },
                {
                    "last_digits": "2222",
                    "total_spent": 100.0,
                    "cashback": 0.0
                }
            ]
        }
    ]
    return tests[request.param]


@pytest.fixture
def df_operations_for_sort(request: Any) -> Any:
    """Данные для тестирования функции src.utils.get_top_five_transactions"""

    date1 = datetime.datetime.strptime("2025-12-01", "%Y-%m-%d")

    tests = [
        {
            "input": pd.DataFrame({
                "Дата платежа": [date1, date1, date1, date1, date1, date1],
                "Сумма операции с округлением": [200.0, 300.0, 100.0, 600.0, 500.0, 400.0],
                "Сумма операции": [-200.0, -300.0, 100.0, -600.0, 500.0, -400.0],
                "Категория": ["Супермаркеты", "Переводы", "Пополнения", "Рестораны", "Пополнения", "Рестораны"],
                "Описание": ["Описание 1", "Описание 2", "Описание 3", "Описание 4", "Описание 5", "Описание 6"]
            }),
            "output": [
                {
                    'date': '01.12.2025',
                    'amount': -600.0,
                    'category': 'Рестораны',
                    'description': 'Описание 4'
                },
                {
                    'date': '01.12.2025',
                    'amount': 500.0,
                    'category': 'Пополнения',
                    'description': 'Описание 5'
                },
                {
                    'date': '01.12.2025',
                    'amount': -400.0,
                    'category': 'Рестораны',
                    'description': 'Описание 6'
                },
                {
                    'date': '01.12.2025',
                    'amount': -300.0,
                    'category': 'Переводы',
                    'description': 'Описание 2'
                },
                {
                    'date': '01.12.2025',
                    'amount': -200.0,
                    'category': 'Супермаркеты',
                    'description': 'Описание 1'
                }
            ]
        }
    ]
    return tests[request.param]


@pytest.fixture
def valute_rates(request: Any) -> Any:
    """Данные для тестирования функции src.external_api.get_currency_rate"""

    mocked_data = {
        "Valute": {
            "USD": {
                "ID": "R01235",
                "NumCode": "840",
                "CharCode": "USD",
                "Nominal": 1,
                "Name": "Доллар США",
                "Value": 78.7135,
                "Previous": 78.5067
            },
            "EUR": {
                "ID": "R01239",
                "NumCode": "978",
                "CharCode": "EUR",
                "Nominal": 1,
                "Name": "Евро",
                "Value": 90.7548,
                "Previous": 90.9438
            },
        }
    }

    tests = [
        {
            "input": {
                "currencies": ["EUR", "USD"],
                "mocked_data": mocked_data
            },
            "output": [{'currency': 'EUR', 'rate': 90.7548}, {'currency': 'USD', 'rate': 78.7135}]
        }
    ]
    return tests[request.param]


@pytest.fixture
def company_share(request: Any) -> Any:
    """Данные для тестирования функции src.external_api.get_stock_price"""

    mocked_data = {
        "Meta Data": {
            "3. Last Refreshed": "2025-06-16",
        },
        "Time Series (Daily)": {
            "2025-06-16": {
                "1. open": "174.7300",
            }
        }
    }

    tests = [
        {
            "input": {
                "company": "GOOGL",
                "mocked_data": mocked_data
            },
            "output": {'stock': 'GOOGL', 'price': 174.73}
        }
    ]
    return tests[request.param]
