import json
from pathlib import Path
from src.config import file_path
from src.utils import reader_transaction_excel, get_user_setting, get_currency_rates, get_stock_price
from src.views import get_expenses_cards, get_greeting, top_transaction, transaction_currency

ROOT_PATH = Path(__file__).resolve().parent.parent


def main(df_transactions, date, user_currencies, user_stocks):
    "Главная функция, делающая вывод на главную страницу"
    greeting = get_greeting()
    transactions = transaction_currency(df_transactions, date)
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


if __name__ == "__main__":
    df_transactions = reader_transaction_excel(str(ROOT_PATH) + file_path)
    date = "29.07.2019 22:06:27"

    user_currencies, user_stocks = get_user_setting(str(ROOT_PATH) + "/user_setting.json")

    date_json = main(df_transactions, date, user_currencies, user_stocks)

    print(date_json)
