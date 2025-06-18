import datetime
import os

import pandas as pd
from dateutil.relativedelta import relativedelta

from src import utils


def spending_by_category(transactions: pd.DataFrame, category: str, date: str | None = None) -> pd.DataFrame:
    """Функция получает на вход датафрейм с транзакциями, категорию операций и дату (опционально).
    Возвращает список транзакций указанной категории за 3 месяца до указанной даты.
    Если дата не указана, то берется текущая дата"""

    if date:
        end_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    else:
        end_date = datetime.datetime.today()

    start_date = end_date + relativedelta(months=-3)
    print(start_date, date)

    filtered_transactions_df = transactions[
        (transactions["Категория"] == category) &
        (transactions["Дата платежа"] > start_date) &
        (transactions["Дата платежа"] <= end_date)
    ]

    return filtered_transactions_df


if __name__ == "__main__":
    df = utils.get_operations(os.path.join('data', 'operations.xlsx'))
    if isinstance(df, pd.DataFrame):
        print(spending_by_category(df, "Пополнения", "2025-12-12"))
