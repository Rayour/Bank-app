import datetime
import os

import pandas
from dateutil.relativedelta import relativedelta

from src import reports, services, utils, views

print("Добро пожаловать в личный кабинет банковского приложения!")
print("""Вы находитесь на Главной странице и, если бы тут был фронт,
созданный на основании красивого дизайна, то вы бы увидели красивый
вывод информации, а пока наслаждайтесь голыми данными""")
today_date = datetime.datetime.now()
print(views.main_view(today_date.strftime("%Y-%m-%d %H:%M:%S")))
print()

operations = utils.get_operations(os.path.join("data", "operations.xlsx"))
if isinstance(operations, pandas.DataFrame):
    last_month = (today_date + relativedelta(months=-1)).month
    year_ = (today_date + relativedelta(months=-1)).year

    print("Сколько кешбека вы могли заработать в прошлом месяце:")
    cashback = services.get_good_cashback_categories(operations, year_, last_month)
    for key, value in cashback.items():
        print(f"{key}: {value} руб.")
    print()

    print("С использованием сервиса Инвесткопилка вы могли бы накопить за прошлый месяц при округлении до 50р:")
    print(round(services.investment_bank_df(operations, f"{year_}-{last_month}", 50), 2))
    print()

    print("Список транзакций с номерами телефонов:")
    print(services.phone_search(operations))
    print()

    print("Список транзакций с переводами физ лицам:")
    print(services.individual_transfer_search(operations))
    print()

    search_str = input("Введите поисковой запрос: ")
    print("Операции, найденные по вашему запросу:")
    print(services.simple_search(operations, search_str))
    print()

    print("Ваши траты за последние 3 месяца:")
    print("По дням недели:")
    spends_weekday = reports.spending_by_weekday(operations).to_dict()
    print(f"Понедельник: {round(spends_weekday["Сумма платежа"]["Monday"], 2)}")
    print(f"Вторник: {round(spends_weekday["Сумма платежа"]["Tuesday"], 2)}")
    print(f"Среда: {round(spends_weekday["Сумма платежа"]["Wednesday"], 2)}")
    print(f"Четверг: {round(spends_weekday["Сумма платежа"]["Thursday"], 2)}")
    print(f"Пятница: {round(spends_weekday["Сумма платежа"]["Friday"], 2)}")
    print(f"Суббота: {round(spends_weekday["Сумма платежа"]["Saturday"], 2)}")
    print(f"Воскресенье: {round(spends_weekday["Сумма платежа"]["Sunday"], 2)}")
    print()
    print("По рабочим/выходным дням:")
    spends_workday = reports.spending_by_workday(operations).to_dict()
    print(f"По рабочим дням: {round(spends_workday["Сумма платежа"]["Рабочий"], 2)}")
    print(f"По выходным: {round(spends_workday["Сумма платежа"]["Выходной"], 2)}")
    print()
    category = input("Укажите категорию для подсчета трат: ")
    print("По категориям:")
    spends_category = reports.spending_by_category(operations, category).to_json(orient='records', force_ascii=False)
    print(spends_category)
