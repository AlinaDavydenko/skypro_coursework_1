import datetime as dt
import logging
from functools import wraps
from pathlib import Path
from typing import Callable

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import get_data

logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/reports.log", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


ROOT_PATH = Path(__file__).resolve().parent.parent


def log(filename: str = "default_report.json") -> Callable:
    """a decorator that logs a function call and its result to a file or to the console"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result: pd.DataFrame = func(*args, **kwargs)
            result.to_json(
                path_or_buf=filename, indent=4, force_ascii=False, orient="records"
            )
            return result

        return wrapper

    return decorator


@log()
def spending_by_category(
    df_transactions: pd.DataFrame, category: str, date: [str] = None
) -> pd.DataFrame:
    """The function returns expenses for a given category for the last three months (from the given date)"""
    if date is None:
        fin_data = dt.datetime.now()
    else:
        fin_data = get_data(date)
    start_data = fin_data.replace(
        hour=0, minute=0, second=0, microsecond=0
    ) - relativedelta(months=3)
    transactions_by_category = df_transactions.loc[
        (pd.to_datetime(df_transactions["Дата операции"], dayfirst=True) <= fin_data)
        & (
            pd.to_datetime(df_transactions["Дата операции"], dayfirst=True)
            >= start_data
        )
        & (df_transactions["Категория"] == category)
    ]
    return transactions_by_category
