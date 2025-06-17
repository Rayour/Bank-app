from typing import Any

import pytest

import src.utils


@pytest.mark.parametrize("hours", [i for i in range(4)], indirect=True)
def test_get_greeting(hours: Any) -> None:
    assert src.utils.get_greeting(hours["input"]) == hours["output"]


@pytest.mark.parametrize("df_operations", [i for i in range(1)], indirect=True)
def test_get_cards_total_info(df_operations: Any) -> None:
    assert src.utils.get_cards_total_info(*df_operations["input"]) == df_operations["output"]
