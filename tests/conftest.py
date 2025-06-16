from typing import Any

import pytest


@pytest.fixture
def hours(request: Any) -> Any:
    """Содержит набор тестовых данных с корректными номерами банковских карт
    для тестирования функции src.views.get_greeting"""

    tests = [
        {"input": "00", "output": "Доброй ночи"},
        {"input": "06", "output": "Доброе утро"},
        {"input": "12", "output": "Добрый день"},
        {"input": "18", "output": "Добрый вечер"},
    ]
    return tests[request.param]
