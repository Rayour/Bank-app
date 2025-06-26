import os

import pandas

from src import external_api, utils


def main_view(date_str: str) -> dict:
    """Функция принимает на вход строку с датой в формате YYYY-MM-DD HH:MM:SS,
    возвращает json с данными о
    1. сообщении приветствия пользователя
    2. данными по расходам карт за период с начала текущего месяца до указанной даты
    3. топ-5 транзакций по величине операций
    4. курсы валют
    5. стоимость акций"""

    user_settings = utils.get_user_settings()

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
