import datetime
import logging
import os
from functools import wraps
from pathlib import Path
from typing import Any, Callable

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
logger = logging.getLogger("decorators")


def print_results(func: Callable) -> Callable:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> Any:
        try:
            result = func(*args, **kwargs)
            print(result.to_dict())
            logger.info(f"Результат работы отчета {func.__name__} выведен в консоль")
        except Exception as e:
            logger.critical(f"Работа отчета {func.__name__} завершилась с ошибкой: {e}")
        return result
    return inner


def write_results(file_path: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            full_file_path = os.path.join(ROOT_PATH, file_path)
            try:
                with open(full_file_path, 'a', encoding='utf-8') as file:
                    file.write(f"{result.to_dict()}\n\n")
                    logger.info(f"Результат работы отчета {func.__name__} записан в файл {full_file_path}")
            except Exception as e:
                logger.critical(
                    f"Не удается записать результат отчета {func.__name__} в файл {full_file_path}. Ошибка: {e}"
                )
            return result
        return inner
    return wrapper
