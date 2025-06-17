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
def df_operations(request: Any) -> Any:
    """Данные для тестирования функции src.utils.get_cards_total_info"""

    date1 = datetime.datetime.strptime("2025-12-01", "%Y-%m-%d")
    date2 = datetime.datetime.strptime("2025-12-02", "%Y-%m-%d")

    tests = [
        {
            "input": (pd.DataFrame({
                "Дата платежа": [date1, date1, date1, date1, date2],
                "Статус": ["OK", "OK", "OK", "FAILED", "OK"],
                "Сумма платежа": [-100.0, -100.0, 100.0, -100.0, -100.0],
                "Номер карты": ["*1111", "*2222", "*1111", "*2222", "*2222"],
                "Кэшбэк": [1.0, 0.0, 1.0, 1.0, 1.0]
            }), "2025-12-01"),
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
