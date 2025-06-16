import datetime
import logging
import os.path
from pathlib import Path

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
logger = logging.getLogger("views")


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
