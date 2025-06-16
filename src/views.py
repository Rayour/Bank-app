import datetime


def get_greeting() -> str:
    """Функция возвращает текст приветствия в зависимости от текущего времени"""

    time_now = int(datetime.datetime.now().strftime('%H'))
    if 0 <= time_now < 6:
        greeting = "Доброй ночи"
    elif 6 <= time_now < 12:
        greeting = "Доброе утро"
    elif 12 <= time_now < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    return greeting


