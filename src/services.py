import datetime
import logging
import os
from pathlib import Path

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


if __name__ == "__main__":
    operations = utils.get_operations(os.path.join("data", "operations.xlsx"))
    if isinstance(operations, pd.DataFrame):
        print(get_good_cashback_categories(operations, 2024, 6))
