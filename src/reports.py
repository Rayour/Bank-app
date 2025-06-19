import datetime
import os
import logging
import pandas as pd
from dateutil.relativedelta import relativedelta
from pathlib import Path

from src import utils

ROOT_PATH = Path(__file__).resolve().parents[1]
date_today = datetime.datetime.today().strftime("%d-%m-%Y")
file_name = f"{date_today}_logs.log"
log_path = os.path.join(ROOT_PATH, "logs", file_name)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=log_path,
    filemode="a",
    encoding="utf-8",
)
logger = logging.getLogger("reports")


def spending_by_category(transactions: pd.DataFrame, category: str, date: str | None = None) -> pd.DataFrame:
    """Функция получает на вход датафрейм с транзакциями, категорию операций и дату (опционально).
    Возвращает список транзакций указанной категории за 3 месяца до указанной даты.
    Если дата не указана, то берется текущая дата"""

    if date:
        end_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    else:
        end_date = datetime.datetime.today()

    start_date = end_date + relativedelta(months=-3)

    logger.info(f"Получаем список транзакций для категории {category} в период с {start_date.strftime("%d.%m.%Y")} \
по {end_date.strftime("%d.%m.%Y")}")
    filtered_transactions_df = transactions[
        (transactions["Категория"] == category) &
        (transactions["Дата платежа"] > start_date) &
        (transactions["Дата платежа"] <= end_date)
        ]

    return filtered_transactions_df


def spending_by_weekday(transactions: pd.DataFrame, date: str | None = None) -> pd.DataFrame:
    """Функция получает на вход датафрейм с транзакциями и опционально дату.
    Возвращает средний размер трат по дням недели за последние 3 месяца с указанной даты.
    Если дата не указана - берется текущая"""

    if date:
        end_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    else:
        end_date = datetime.datetime.today()

    start_date = end_date + relativedelta(months=-3)

    logger.info(
        f"Получаем список расходов в период с {start_date.strftime("%d.%m.%Y")} по {end_date.strftime("%d.%m.%Y")}")
    filtered_transactions_df = transactions[
        (transactions["Сумма платежа"] < 0) &
        (transactions["Дата платежа"] > start_date) &
        (transactions["Дата платежа"] <= end_date) &
        (transactions["Статус"] == "OK")
        ]
    logger.info(
        f"Формируем отчет по тратам по дням недели в период с {start_date.strftime("%d.%m.%Y")} \
по {end_date.strftime("%d.%m.%Y")}")
    filtered_transactions_df["День недели"] = filtered_transactions_df["Дата платежа"].map(lambda x: x.strftime('%A'))
    current_df = filtered_transactions_df.loc[:, ["День недели", "Сумма платежа"]]
    spending_by_weekday_df = current_df.groupby("День недели").mean()

    return spending_by_weekday_df


def spending_by_workday(transactions: pd.DataFrame, date: str | None = None) -> pd.DataFrame:
    """Функция получает на вход датафрейм с транзакциями и опционально дату.
    Возвращает средний размер трат по рабочим и выходнымдням недели за последние 3 месяца с указанной даты.
    Если дата не указана - берется текущая"""

    if date:
        end_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    else:
        end_date = datetime.datetime.today()

    start_date = end_date + relativedelta(months=-3)

    logger.info(
        f"Получаем список расходов в период с {start_date.strftime("%d.%m.%Y")} по {end_date.strftime("%d.%m.%Y")}")
    filtered_transactions_df = transactions[
        (transactions["Сумма платежа"] < 0) &
        (transactions["Дата платежа"] > start_date) &
        (transactions["Дата платежа"] <= end_date) &
        (transactions["Статус"] == "OK")
        ]
    logger.info(
        f"Формируем отчет по тратам по рабочим/выходным дням в период с {start_date.strftime("%d.%m.%Y")} \
по {end_date.strftime("%d.%m.%Y")}")
    filtered_transactions_df["Рабочий/выходной день"] = filtered_transactions_df["Дата платежа"].map(
        lambda x: "Выходной" if int(x.strftime('%w')) % 6 == 0 else "Рабочий"
    )
    current_df = filtered_transactions_df.loc[:, ["Рабочий/выходной день", "Сумма платежа"]]
    spending_by_workday_df = current_df.groupby("Рабочий/выходной день").mean()

    return spending_by_workday_df


if __name__ == "__main__":
    df = utils.get_operations(os.path.join('data', 'operations.xlsx'))
    if isinstance(df, pd.DataFrame):
        print(spending_by_category(df, "Пополнения", "2025-12-12"))
        print(spending_by_weekday(df).to_dict())
        print(spending_by_workday(df).to_dict())
