from typing import Any

import pytest

import src.views


@pytest.mark.parametrize("hours", [i for i in range(4)], indirect=True)
def test_get_greeting(hours: Any) -> None:
    assert src.views.get_greeting(hours["input"]) == hours["output"]
