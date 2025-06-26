import os
from pathlib import Path
from typing import Any

import pandas as pd

import src.decorators

ROOT_PATH = Path(__file__).resolve().parents[1]


def test_print_results(capsys: Any) -> None:
    @src.decorators.print_results
    def get_df() -> pd.DataFrame:
        return pd.DataFrame({"test": [1, 2]})

    get_df()
    stream = capsys.readouterr().out
    assert stream == "{'test': {0: 1, 1: 2}}\n"


def test_write_results() -> None:
    @src.decorators.write_results(os.path.join("tests", "reports", "results.txt"))
    def get_df() -> pd.DataFrame:
        return pd.DataFrame({"test": [1, 2]})

    file_path = os.path.join(ROOT_PATH, "tests", "reports", "results.txt")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("")
    get_df()
    with open(file_path, 'r', encoding='utf-8') as file:
        result = file.read()

    assert result == "{'test': {0: 1, 1: 2}}\n\n"
