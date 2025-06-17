import datetime
import json
import logging
import os.path
from pathlib import Path

import pandas
import pandas as pd

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
logger = logging.getLogger("utils")


def get_greeting(hours: str) -> str:
    """Функция возвращает текст приветствия в зависимости от текущего времени"""

    time_now = int(hours)
    if 0 <= time_now < 6:
        greeting = "Доброй ночи"
    elif 6 <= time_now < 12:
        greeting = "Доброе утро"
    elif 12 <= time_now < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    logger.info(f"Определено приветствие для времени {hours} (час): {greeting}")
    return greeting


def get_operations(file_path: str) -> pd.DataFrame | None:
    """Функция читает данные из .xlsx файла с операциями и возвращает датафрейм"""

    full_path = os.path.join(ROOT_PATH, file_path)
    try:
        logger.info(f"Попытка чтения операций из файла {full_path}")
        operations_df = pd.read_excel(full_path)
    except Exception as e:
        logger.critical(f"Не удалось прочитать файл {full_path}: {e}")
        return None
    else:
        logger.info(f"Файл {full_path} успешно прочитан")
        return operations_df


def get_df_by_dates(df: pd.DataFrame, date_: str) -> pd.DataFrame:
    """Функция получает датафрейм с данными,
    фильтрует только те операции, дата которых в промежутке с начала месяца до указанной даты"""

    end_date = datetime.datetime.strptime(date_, "%Y-%m-%d")
    start_date = end_date.replace(day=1)

    logger.info(f"Получаем список расходов с начала месяца по {date_}")
    df_current_date = df[(start_date <= df["Дата платежа"]) & (end_date >= df["Дата платежа"])]
    return df_current_date


def get_cards_total_info(df: pd.DataFrame) -> list[dict]:
    """Функция получает датафрейм с информацией об операциях,
    возвращает список карт с суммарной информацией по расходам и кешбеку"""

    logger.info("Получаем список расходов по успешным операциям")
    df_spend_status_ok = df[(df["Статус"] == "OK") & (df["Сумма платежа"] < 0)].loc[df["Номер карты"].notnull()]

    logger.info("Рассчитываем сумму расходов по картам")
    df_cards_spend = df_spend_status_ok.groupby("Номер карты")["Сумма платежа"].sum()

    logger.info("Рассчитываем кэшбек по картам")
    df_cards_cashback = df_spend_status_ok.groupby("Номер карты")["Кэшбэк"].sum()

    cards_dict_spend = df_cards_spend.to_dict()
    cards_dict_cashback = df_cards_cashback.to_dict()
    cards_list = []

    logger.info("Формируем список с данными по картам")
    for key in cards_dict_spend.keys():
        card = {
            "last_digits": key[1:],
            "total_spent": abs(round(cards_dict_spend[key], 2)),
            "cashback": round(cards_dict_cashback[key], 2)
        }

        cards_list.append(card)

    return cards_list


def get_top_five_transactions(df: pd.DataFrame) -> list[dict]:
    """Функция получает датафрейм с данными и дату для выборки,
    возвращает топ-5 транзакций по сумме платежа за период с начала месяца до указанной даты"""

    sorted_df = df.sort_values("Сумма операции с округлением", ascending=False)
    top_five_df = sorted_df.iloc[0:5]
    top_five_operations_full_list = json.loads(top_five_df.to_json(orient='records'))
    top_five_operations_list = []

    for operation in top_five_operations_full_list:
        ts = operation["Дата платежа"] // 1000
        short_operation = {
            "date": datetime.datetime.fromtimestamp(ts, datetime.UTC).strftime("%d.%m.%Y"),
            "amount": operation["Сумма операции"],
            "category": operation["Категория"],
            "description": operation["Описание"]
        }
        top_five_operations_list.append(short_operation)

    return top_five_operations_list


if __name__ == "__main__":
    df = get_operations(os.path.join('data', 'operations.xlsx'))
    if isinstance(df, pandas.DataFrame):
        current_df = get_df_by_dates(df, "2025-12-11")
        print(get_cards_total_info(current_df))
        print(get_top_five_transactions(current_df))
