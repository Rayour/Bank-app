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
                "Value": 78.7135,
            },
            "EUR": {
                "Value": 90.7548,
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


@pytest.fixture
def df_operations_for_cashback(request: Any) -> Any:
    """Данные для тестирования функции src.services.get_good_cashback_categories"""

    date1 = datetime.datetime.strptime("2025-12-01", "%Y-%m-%d")

    tests = [
        {
            "input": (pd.DataFrame({
                "Дата платежа": [date1, date1, date1, date1],
                "Сумма платежа": [-200.0, 100.0, -400.0, -600.0],
                "Категория": ["Супермаркеты", "Пополнения", "Переводы", "Рестораны"],
                "Статус": ["OK", "OK", "OK", "FAILED"],
            }), 2025, 12),
            "output": {
                "Супермаркеты": 2,
                "Переводы": 4,
            }
        }
    ]
    return tests[request.param]


@pytest.fixture
def transactions_list(request: Any) -> Any:
    """Данные для тестирования функции src.services.investment_bank"""

    transactions = [
        {
            "date": "2025-12-01",
            "amount": -245.5
        },
        {
            "date": "2025-12-02",
            "amount": -215.5
        },
        {
            "date": "2025-11-01",
            "amount": -205.5
        },
        {
            "date": "2025-12-01",
            "amount": 245.5
        },
    ]

    tests = [
        {
            "input": ("2025-12", transactions, 50),
            "output": 39.0
        }
    ]
    return tests[request.param]


@pytest.fixture
def df_operations_for_simple_search(request: Any) -> Any:
    """Данные для тестирования функции src.services.simple_search"""

    tests = [
        {
            "input": (pd.DataFrame({
                "Категория": ["Супермаркеты", "Маркетплейсы", "Переводы", "Рестораны"],
                "Описание": ["Перекресток", "Wildberries", "Мартышка", "Заглушка"],
            }), "мар"),
            "output": [
                {
                    "Категория": "Супермаркеты",
                    "Описание": "Перекресток",
                },
                {
                    "Категория": "Маркетплейсы",
                    "Описание": "Wildberries",
                },
                {
                    "Категория": "Переводы",
                    "Описание": "Мартышка",
                }
            ]
        }
    ]
    return tests[request.param]


@pytest.fixture
def df_operations_for_phone_search(request: Any) -> Any:
    """Данные для тестирования функции src.services.phone_search"""

    tests = [
        {
            "input": pd.DataFrame({
                "Описание": [
                    "Я МТС +7 921 111-22-33",
                    "Тинькофф Мобайл +7 995 555-55-55",
                    "МТС Mobile +7 981 333-44-55",
                    "Заглушка"
                ],
            }),
            "output": [
                {
                    "Описание": "Я МТС +7 921 111-22-33",
                },
                {
                    "Описание": "Тинькофф Мобайл +7 995 555-55-55",
                },
                {
                    "Описание": "МТС Mobile +7 981 333-44-55",
                }
            ]
        }
    ]
    return tests[request.param]


@pytest.fixture
def df_operations_for_individual_transfer_search(request: Any) -> Any:
    """Данные для тестирования функции src.services.individual_transfer_search"""

    tests = [
        {
            "input": pd.DataFrame({
                "Категория": ["Переводы", "Переводы", "Переводы", "Рестораны"],
                "Описание": ["Константинопольский К.", "Иванов И.", "В организацию", "Заглушка"],
            }),
            "output": [
                {
                    "Категория": "Переводы",
                    "Описание": "Константинопольский К.",
                },
                {
                    "Категория": "Переводы",
                    "Описание": "Иванов И.",
                }
            ]
        }
    ]
    return tests[request.param]


@pytest.fixture
def df_operations_for_spending_by_category(request: Any) -> Any:
    """Данные для тестирования функции src.reports.spending_by_category"""

    date1 = datetime.datetime.strptime("2025-12-05", "%Y-%m-%d")
    date2 = datetime.datetime.strptime("2025-11-05", "%Y-%m-%d")
    date3 = datetime.datetime.strptime("2025-10-05", "%Y-%m-%d")
    date4 = datetime.datetime.strptime("2025-09-05", "%Y-%m-%d")

    tests = [
        {
            "input": (pd.DataFrame({
                "Дата платежа": [date1, date2, date3, date4],
                "Категория": ["Рестораны", "Пополнения", "Переводы", "Рестораны"],
            }), "Пополнения", "2025-12-10"),
            "output": {
                "Дата платежа": {1: date2},
                "Категория": {1: "Пополнения"}
            }
        }
    ]
    return tests[request.param]


@pytest.fixture
def df_operations_for_spending_groups() -> Any:
    """Входные данные для тестирования функции src.reports.spending_by_weekday и src.reports.spending_by_workday"""

    date1 = datetime.datetime.strptime("2025-12-15", "%Y-%m-%d")
    date2 = datetime.datetime.strptime("2025-11-03", "%Y-%m-%d")
    date3 = datetime.datetime.strptime("2025-11-04", "%Y-%m-%d")
    date4 = datetime.datetime.strptime("2025-11-05", "%Y-%m-%d")
    date5 = datetime.datetime.strptime("2025-11-06", "%Y-%m-%d")
    date6 = datetime.datetime.strptime("2025-11-07", "%Y-%m-%d")
    date7 = datetime.datetime.strptime("2025-11-08", "%Y-%m-%d")
    date8 = datetime.datetime.strptime("2025-11-09", "%Y-%m-%d")
    date9 = datetime.datetime.strptime("2025-11-10", "%Y-%m-%d")
    date10 = datetime.datetime.strptime("2025-11-11", "%Y-%m-%d")
    date11 = datetime.datetime.strptime("2025-11-12", "%Y-%m-%d")
    date12 = datetime.datetime.strptime("2025-11-13", "%Y-%m-%d")
    date13 = datetime.datetime.strptime("2025-11-14", "%Y-%m-%d")
    date14 = datetime.datetime.strptime("2025-11-15", "%Y-%m-%d")
    date15 = datetime.datetime.strptime("2025-11-16", "%Y-%m-%d")

    df = pd.DataFrame({
        "Дата платежа": [date1, date2, date3, date4, date5, date6, date7, date8, date9, date10, date11, date12, date13,
                         date14, date14, date15, date15],
        "Сумма платежа": [-200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -100.0, -100.0, -100.0,
                          -100.0, -100.0, -100.0, 100.0, -100.0, -100.0],
        "Статус": ["OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK",
                   "FAILED"],
    })

    return df, "2025-12-10"


@pytest.fixture
def output_data_for_report_by_weekdays() -> dict:
    """Выходные данные для тестирования функции src.reports.spending_by_weekday"""
    return {
        'Сумма платежа': {'Friday': -150.0, 'Monday': -150.0, 'Saturday': -150.0,
                          'Sunday': -150.0, 'Thursday': -150.0, 'Tuesday': -150.0,
                          'Wednesday': -150.0}}


@pytest.fixture
def output_data_for_report_by_workdays() -> dict:
    """Выходные данные для тестирования функции src.reports.spending_by_weekday"""
    return {'Сумма платежа': {'Выходной': -150.0, 'Рабочий': -150.0}}


@pytest.fixture
def df_operations_for_invest_bank() -> Any:
    """Входные данные для тестирования функции src.reports.spending_by_weekday и src.reports.investment_bank_df"""

    date1 = datetime.datetime.strptime("2025-12-15", "%Y-%m-%d")
    date2 = datetime.datetime.strptime("2025-11-03", "%Y-%m-%d")
    date3 = datetime.datetime.strptime("2025-11-04", "%Y-%m-%d")
    date4 = datetime.datetime.strptime("2025-11-05", "%Y-%m-%d")
    date5 = datetime.datetime.strptime("2025-11-06", "%Y-%m-%d")
    date6 = datetime.datetime.strptime("2025-11-07", "%Y-%m-%d")

    df = pd.DataFrame({
        "Дата платежа": [date1, date2, date3, date4, date5, date6],
        "Сумма платежа": [-105.0, -110.0, -115.0, -120.0, 200.0, -200.0],
        "Статус": ["OK", "OK", "OK", "OK", "OK", "FAILED"],
    })

    return {"input": (df, "2025-11", 50), "output": 105.0}
