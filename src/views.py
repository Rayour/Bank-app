import datetime
import json
import logging
import os
from pathlib import Path

import pandas

from src import external_api, utils

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
logger = logging.getLogger("view")


def main_view(date_str: str) -> dict:
    """Функция принимает на вход строку с датой в формате YYYY-MM-DD HH:MM:SS,
    возвращает json с данными о
    1. сообщении приветствия пользователя
    2. данными по расходам карт за период с начала текущего месяца до указанной даты
    3. топ-5 транзакций по величине операций
    4. курсы валют
    5. стоимость акций"""

    user_settings_url = os.path.join(ROOT_PATH, 'user_settings.json')
    logger.info("Получение пользовательских настроек...")
    try:
        logger.info(f"Попытка чтения файла {user_settings_url}")
        with open(user_settings_url, "r", encoding="utf-8") as json_file:
            logger.info(f"Получение JSON из файла {user_settings_url}")
            user_settings = json.load(json_file)
    except FileNotFoundError:
        logger.error(f"Файл {user_settings} не найден. Настройки пользователя будут пустыми.")
        user_settings = json.loads('{"user_currencies": [], "user_stocks": []}')

    date_date = date_str[:10]
    date_time_hours = date_str[11:13]

    greeting = utils.get_greeting(date_time_hours)
    operations = utils.get_operations(os.path.join("data", "operations.xlsx"))
    if isinstance(operations, pandas.DataFrame):
        current_operations = utils.get_df_by_dates(operations, date_date)
        cards = utils.get_cards_total_info(current_operations)
        top_transactions = utils.get_top_five_transactions(current_operations)
    else:
        cards = []
        top_transactions = []
    currency_rates = external_api.get_currency_rate(user_settings["user_currencies"])
    user_stocks = user_settings["user_stocks"]
    stock_prices = []
    for stock in user_stocks:
        stock_prices.append(external_api.get_stock_price(stock))

    result = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    return result


if __name__ == "__main__":
    print(main_view("2025-12-12 18:13:43"))
