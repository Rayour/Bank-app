import datetime
import logging
import os.path
from pathlib import Path

import requests

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
logger = logging.getLogger("external_api")


def get_currency_rate(currencies: list) -> list[dict]:
    """Получает на вход список валют, возвращает список словарей с информацией о текущем курсе"""

    rates = []
    try:
        logger.info("Запрос курсов валют...")
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.critical(f"При запросе курсов валют произошла ошибка: {e}")
    else:
        logger.info("Формирование списка курсов валют...")
        result = response.json()
        for currency in currencies:
            if currency in result["Valute"]:
                currency_rate = {
                    "currency": currency,
                    "rate": result["Valute"][currency]["Value"]
                }
                rates.append(currency_rate)
    finally:
        logger.info("Получен список курсов валют...")
        return rates


if __name__ == "__main__":
    print(get_currency_rate(["EUR", "USD"]))
