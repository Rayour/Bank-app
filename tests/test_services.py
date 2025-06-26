import json
from typing import Any

import pytest

import src.services


@pytest.mark.parametrize("df_operations_for_cashback", [i for i in range(1)], indirect=True)
def test_get_good_cashback_categories(df_operations_for_cashback: Any) -> None:
    assert src.services.get_good_cashback_categories(*df_operations_for_cashback["input"]) == \
        df_operations_for_cashback["output"]


@pytest.mark.parametrize("transactions_list", [i for i in range(1)], indirect=True)
def test_investment_bank(transactions_list: Any) -> None:
    assert src.services.investment_bank(*transactions_list["input"]) == transactions_list["output"]


def test_investment_bank_df(df_operations_for_invest_bank: Any) -> None:
    assert src.services.investment_bank_df(*df_operations_for_invest_bank["input"]) == \
           df_operations_for_invest_bank["output"]


@pytest.mark.parametrize("df_operations_for_simple_search", [i for i in range(1)], indirect=True)
def test_simple_search(df_operations_for_simple_search: Any) -> None:
    assert json.loads(src.services.simple_search(*df_operations_for_simple_search["input"])) == \
           df_operations_for_simple_search["output"]


@pytest.mark.parametrize("df_operations_for_phone_search", [i for i in range(1)], indirect=True)
def test_phone_search(df_operations_for_phone_search: Any) -> None:
    assert json.loads(src.services.phone_search(df_operations_for_phone_search["input"])) == \
           df_operations_for_phone_search["output"]


@pytest.mark.parametrize("df_operations_for_individual_transfer_search", [i for i in range(1)], indirect=True)
def test_individual_transfer_search(df_operations_for_individual_transfer_search: Any) -> None:
    assert json.loads(
        src.services.individual_transfer_search(df_operations_for_individual_transfer_search["input"])
    ) == df_operations_for_individual_transfer_search["output"]
