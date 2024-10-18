import datetime
import datetime as dt
import logging
from pathlib import Path
import pandas as pd
from src.utils import get_data
from functools import wraps
from typing import Any, Callable


logger = logging.getLogger("logs")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("..\\logs\\reports.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


ROOT_PATH = Path(__file__).resolve().parent.parent


def log(filename: Any = None) -> Callable:
    """a decorator that logs a function call and its result to a file or to the console"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                log_messege = "my_function ok\n"
            except Exception as e:
                result = None
                log_messege = f"my_function error: {e}. Inputs: {args}, {kwargs} \n"
            if filename:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(log_messege)
            else:
                print(log_messege)
                return result

        return wrapper

    return decorator


def spending_by_category(df_transactions: pd.DataFrame, category: str, date: [str] = None) -> pd.DataFrame:
    """The function returns expenses for a given category for the last three months (from the given date)"""
    if date is None:
        fin_data = dt.datetime.now()
    else:
        fin_data = get_data(date)
    start_data = fin_data.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=91)
    transactions_by_category = df_transactions.loc[
        (pd.to_datetime(df_transactions["Date operations"], dayfirst=True) <= fin_data)
        & (pd.to_datetime(df_transactions["Date operations"], dayfirst=True) >= start_data)
        & (df_transactions["Category"] == category)
    ]
    return transactions_by_category
