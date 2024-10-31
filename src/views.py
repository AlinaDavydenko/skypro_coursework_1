# Function for the Home page
import json
import logging
from pathlib import Path

from src.utils import (
    get_currency_rates,
    get_expenses_cards,
    get_greeting,
    get_stock_price,
    top_transaction,
    transaction_currency,
)

ROOT_PATH = Path(__file__).resolve().parent.parent


logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/views.log", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main(df_transactions, date, user_currencies, user_stocks):
    "Главная функция, делающая вывод на главную страницу"
    greeting = get_greeting()
    filtered_transactions = transaction_currency(df_transactions, date)
    cards = get_expenses_cards(filtered_transactions)
    top_trans = top_transaction(filtered_transactions)
    currency_rates = get_currency_rates(user_currencies)
    stock_prices = get_stock_price(user_stocks)

    date_json = json.dumps(
        {
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_trans,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        },
        indent=4,
        ensure_ascii=False,
    )
    return date_json
