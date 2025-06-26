import datetime
import logging
import os.path
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

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


def get_stock_price(company_code: str) -> dict | None:
    """Получает на вход код компании, возвращает стоимость акции"""

    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": company_code,
        "apikey": api_key
    }

    try:
        logger.info(f"Запрос стоимости акций для {company_code}")
        response = requests.get(url=url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.critical(f"При запросе стоимости акций для {company_code} произошла ошибка: {e}")
        return None
    else:
        logger.info(f"Формирование информации о стоимости акций для {company_code}")
        result = response.json()
        refresh_date = result["Meta Data"]["3. Last Refreshed"]
        price = {
            "stock": company_code,
            "price": round(float(result["Time Series (Daily)"][refresh_date]["1. open"]), 2)
        }
        return price


if __name__ == "__main__":
    print(get_currency_rate(["EUR", "USD"]))
    print(get_stock_price("AMZN"))
