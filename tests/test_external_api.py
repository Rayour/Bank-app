from typing import Any
from unittest.mock import patch

import pytest

import src.external_api


@pytest.mark.parametrize("valute_rates", [i for i in range(1)], indirect=True)
@patch("requests.get")
def test_get_currency_rate(mocked_get: Any, valute_rates: Any) -> None:
    mocked_get.return_value.json.return_value = valute_rates["input"]["mocked_data"]
    assert src.external_api.get_currency_rate(valute_rates["input"]["currencies"]) == valute_rates["output"]
