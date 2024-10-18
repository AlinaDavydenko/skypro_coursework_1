# Function for the Home page
import logging
from pathlib import Path
import json
from src.utils import (
    get_data,
    reader_transaction_excel,
    top_transaction,
    transaction_currency,
    get_expenses_cards,
    get_currency_rates,
    get_stock_price,
    get_greeting,
)

ROOT_PATH = Path(__file__).resolve().parent.parent


logger = logging.getLogger("logs")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("..\\logs\\views.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main(df_transactions, user_currencies, user_stocks):
    """ The main function that outputs to the main page """
    greeting = get_greeting()
    # transactions = transaction_currency(df_transactions, date)
    cards = get_expenses_cards(df_transactions)
    top_trans = top_transaction(df_transactions)
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
