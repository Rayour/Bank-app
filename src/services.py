import datetime
import logging
import os
import re
from pathlib import Path
from typing import Any

import pandas as pd
from dateutil.relativedelta import relativedelta

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
logger = logging.getLogger("services")


def get_good_cashback_categories(data: pd.DataFrame, year: int, month: int) -> dict:
    """Функция получает датафрейм с операциями, год и месяц для анализа,
    возвращает словарь с анализом, сколько кешбека можно было получить по каждой категории трат"""

    first_next_month_day = datetime.datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d") + relativedelta(months=1)
    last_month_day = (first_next_month_day + datetime.timedelta(seconds=-1)).strftime("%Y-%m-%d")

    logger.info(f"Получаем список операций для месяца {month}.{year}")
    current_month_df = utils.get_df_by_dates(data, last_month_day)

    logger.info(f"Получаем список расходов для месяца {month}.{year}")
    spend_operations_df = current_month_df[
        (current_month_df["Статус"] == "OK") & (current_month_df["Сумма платежа"] < -100)]

    logger.info(f"Формируем данные по категориям для месяца {month}.{year}")
    spend_categories_df = spend_operations_df.groupby("Категория")["Сумма платежа"].sum()

    spends_dict = spend_categories_df.to_dict()
    for key, value in spends_dict.items():
        spends_dict[key] = int(value / -100)

    return spends_dict


def investment_bank(month: str, transactions: list[dict], limit: int) -> float:
    """Функция получает месяц ('YYYY-MM'), список транзакций и лимит округления.
    Возвращает сумму, которую можно было бы накопить за данный месяц с указанным лимитом."""

    save_sum = 0.0

    for transaction in transactions:
        if transaction["date"][:7] == month and transaction["amount"] < 0:
            save_sum += transaction["amount"] % limit

    return save_sum


def investment_bank_df(df_: pd.DataFrame, month: str, limit: int) -> Any:
    """Функция получает датафрейм со списком транзакций, месяц ('YYYY-MM') и лимит округления.
    Возвращает сумму, которую можно было бы накопить за данный месяц с указанным лимитом."""

    first_next_month_day = datetime.datetime.strptime(f"{month}-01", "%Y-%m-%d") + relativedelta(months=1)
    last_month_day = (first_next_month_day + datetime.timedelta(seconds=-1)).strftime("%Y-%m-%d")

    logger.info(f"Получаем список операций для месяца {month}")
    current_month_df = utils.get_df_by_dates(df_, last_month_day)

    logger.info(f"Получаем список расходов для месяца {month}")
    spend_operations_df = current_month_df[
        (current_month_df["Статус"] == "OK") & (current_month_df["Сумма платежа"] < 0)]

    logger.info(f"Рассчитываем накопления за месяц {month}")
    spend_operations_df.loc[:, ["Накопления"]] = spend_operations_df["Сумма платежа"].map(lambda x: x % limit)
    save_amount = spend_operations_df["Накопления"].sum()
    return save_amount


def simple_search(df_: pd.DataFrame, search_str: str) -> str:
    """Функция получает на вход датафрейм с транзакциями и строку для поиска.
    Возвращает json с транзакциями, в описании или категории которых найдено переданное значение."""

    logger.info(f"Формируем список транзакций с упоминанием {search_str} в категории или описании")
    data = df_
    data["Совпадение_описание"] = data["Описание"].map(lambda x: bool(re.search(search_str, x, flags=re.IGNORECASE)))
    data["Совпадение_категория"] = \
        data["Категория"].map(lambda x: bool(re.search(search_str, str(x), flags=re.IGNORECASE)))
    filtered_df = data[data["Совпадение_описание"] | data["Совпадение_категория"]].iloc[:, :-2]

    return filtered_df.to_json(orient='records', force_ascii=False)


def phone_search(df_: pd.DataFrame) -> str:
    """Функция получает на вход датафрейм с транзакциями.
    Возвращает json с транзакциями, в описании которых найден номер телефона."""

    logger.info("Формируем список транзакций номерами телефонов")
    data = df_
    data["Совпадение"] = data["Описание"].map(lambda x: bool(re.search(r"\+7\s\d{3}\s\d{3}-\d{2}-\d{2}", x)))
    filtered_df = data[data["Совпадение"]].iloc[:, :-1]

    return filtered_df.to_json(orient='records', force_ascii=False)


def individual_transfer_search(df_: pd.DataFrame) -> str:
    """Функция получает на вход датафрейм с транзакциями.
    Возвращает json с транзакциями категории "Переводы", в описании которых найдена фамилия и первая буква имени."""

    logger.info("Формируем список транзакций с переводами физическим лицам")
    df_transfers = df_[df_["Категория"] == "Переводы"]
    df_transfers.loc[:, ["Совпадение"]] = \
        df_["Описание"].map(lambda x: bool(re.match(r"^[А-Яа-яЁё]+\s[А-Я]{1}\.$", x)))
    filtered_df = df_transfers[df_transfers["Совпадение"]].iloc[:, :-1]

    return filtered_df.to_json(orient='records', force_ascii=False)


if __name__ == "__main__":
    # operations = utils.get_operations(os.path.join("data", "operations.xlsx"))
    # if isinstance(operations, pd.DataFrame):
    #    print(get_good_cashback_categories(operations, 2024, 6))
    df = utils.get_operations(os.path.join('data', 'operations.xlsx'))
    if isinstance(df, pd.DataFrame):
        # print(simple_search(df, "марк"))
        # print(phone_search(df))
        print(investment_bank_df(df, '2025-12', 100))
