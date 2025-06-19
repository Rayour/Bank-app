from typing import Any

import pytest

import src.reports


@pytest.mark.parametrize("df_operations_for_spending_by_category", [i for i in range(1)], indirect=True)
def test_spending_by_category(df_operations_for_spending_by_category: Any) -> None:
    assert src.reports.spending_by_category(*df_operations_for_spending_by_category["input"]).to_dict() == \
           df_operations_for_spending_by_category["output"]


def test_spending_by_weekday(df_operations_for_spending_groups: tuple,
                             output_data_for_report_by_weekdays: dict) -> None:
    assert src.reports.spending_by_weekday(*df_operations_for_spending_groups).to_dict() == \
           output_data_for_report_by_weekdays


def test_spending_by_workday(df_operations_for_spending_groups: tuple,
                             output_data_for_report_by_workdays: dict) -> None:
    assert src.reports.spending_by_workday(*df_operations_for_spending_groups).to_dict() == \
           output_data_for_report_by_workdays
