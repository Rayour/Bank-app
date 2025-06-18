from typing import Any

import pytest

import src.services


@pytest.mark.parametrize("df_operations_for_cashback", [i for i in range(1)], indirect=True)
def test_get_good_cashback_categories(df_operations_for_cashback: Any) -> None:
    assert src.services.get_good_cashback_categories(*df_operations_for_cashback["input"]) == \
        df_operations_for_cashback["output"]
