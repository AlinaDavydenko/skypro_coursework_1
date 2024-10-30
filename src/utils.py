# Helper functions required for the Home page function to work
import datetime
import datetime as dt
import json
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/utils.log", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_data(data: str) -> datetime.datetime:
    """Date Conversion Function"""
    logger.info(f"Received date string: {data}")
    try:
        data_obj = datetime.datetime.strptime(data, "%d.%m.%Y %H:%M:%S")
        logger.info(f"Converted to object datetime: {data_obj}")
        return data_obj
    except ValueError as e:
        logger.error(f"Date conversion error: {e}")
        raise e


def reader_transaction_excel(file_path) -> pd.DataFrame:
    """The function takes a path to a file as input and returns a dataframe"""
    logger.info(f"The function to get transactions from a file was called. {file_path}")
    try:
        df_transactions = pd.read_excel(file_path)
        logger.info(f"File {file_path} found, transaction data received")

        return df_transactions
    except FileNotFoundError:
        logger.info(f"File {file_path} not found")
        raise


def get_dict_transaction(file_path) -> list[dict]:
    """Function converting dataframe to python dictionary"""
    logger.info(f"Function called get_dict_transaction with file {file_path}")
    try:
        df = pd.read_excel(file_path)
        logger.info(f"File {file_path} read")
        dict_transaction = df.to_dict(orient="records")
        logger.info("Dataframe converted to list of dictionaries")
        return dict_transaction
    except FileNotFoundError:
        logger.error(f"File {file_path} not found")
        raise
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise


def get_currency_rates(currencies):
    """function, returns rates"""
    logger.info("The function to get the rates was called")
    api_key = os.environ.get("API_KEY")
    symbols = ",".join(currencies)
    url = f"https://api.apilayer.com/currency_data/live?symbols={symbols}"

    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    if status_code != 200:
        print(f"The request was not successful. Possible reason: {response.reason}")

    else:
        data = response.json()
        quotes = data.get("quotes", {})
        usd = quotes.get("USDRUB")
        eur_usd = quotes.get("USDEUR")
        eur = usd / eur_usd
        logger.info("The function has completed its work.")

        return [
            {"currency": "USD", "rate": round(usd, 2)},
            {"currency": "EUR", "rate": round(eur, 2)},
        ]


def get_stock_price(stocks):
    """Function that returns stock prices"""
    logger.info("The function returning stock prices was called")
    api_key = os.environ.get("API_KEY")
    stock_price = []
    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"The request was not successful. Possible reason: {response.reason}")

        else:
            data_ = response.json()
            stock_price.append(
                {
                    "stock": stock,
                    "price": round(float(data_["Global Quote"]["05. price"]), 2),
                }
            )
    logger.info("The function has completed its work.")
    return stock_price


def top_transaction(df_transactions):
    """Function of displaying top 5 transactions by payment amount"""
    logger.info("Getting started with the function top_transaction")
    top_transaction = df_transactions.sort_values(
        by="Сумма операции", ascending=True
    ).iloc[:5]
    logger.info("Top 5 transactions by payment amount received")
    result_top_transaction = top_transaction.to_dict(orient="records")
    top_transaction_list = []
    for transaction in result_top_transaction:
        top_transaction_list.append(
            {
                "date": str(
                    (
                        datetime.datetime.strptime(
                            transaction["Дата операции"], "%d.%m.%Y %H:%M:%S"
                        )
                    )
                    .date()
                    .strftime("%d.%m.%Y")
                ).replace("-", "."),
                "amount": transaction["Сумма платежа"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )
    logger.info("The list of top 5 transactions has been formed")
    return top_transaction_list


def get_expenses_cards(df_transactions) -> list[dict]:
    """Function that returns expenses for each card"""
    logger.info("Start of function execution get_expenses_cards")

    cards_dict = (
        df_transactions.loc[df_transactions["Сумма операции"] < 0]
        .groupby(by="Номер карты")
        .agg("Сумма операции")
        .sum()
        .to_dict()
    )
    logger.debug(f"Dictionary of card expenses received: {cards_dict}")

    expenses_cards = []
    for card, expenses in cards_dict.items():
        expenses_cards.append(
            {
                "last_digits": card,
                "total spent": abs(expenses),
                "cashback": abs(round(expenses / 100, 2)),
            }
        )
        logger.info(f"Added consumption on the card {card}: {abs(expenses)}")

    logger.info("Completing the function execution get_expenses_cards")
    return expenses_cards


def transaction_currency(df_transactions: pd.DataFrame, data: str) -> pd.DataFrame:
    """function generates expenses in a given interval"""
    logger.info(
        f"Function called transaction_currency with arguments: df_transactions={df_transactions}, data={data}"
    )
    fin_data = get_data(data)
    logger.debug(f"The final date has been received: {fin_data}")
    start_data = fin_data.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    logger.debug(f"End date updated: {fin_data}")
    transaction_currency = df_transactions.loc[
        (pd.to_datetime(df_transactions["Дата операции"], dayfirst=True) <= fin_data)
        & (
            pd.to_datetime(df_transactions["Дата операции"], dayfirst=True)
            >= start_data
        )
    ]
    logger.info(f"Get DataFrame transaction_currency: {transaction_currency}")

    return transaction_currency


def get_greeting():
    """Function - greeting"""
    hour = dt.datetime.now().hour
    if 4 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 22:
        return "Good evening"
    else:
        return "Good night"


def get_user_setting(path):
    """Function for translating user settings (rate and shares) from a json object"""
    logger.info(f"Function called with file {path}")
    with open(path, "r", encoding="utf-8") as f:
        user_setting = json.load(f)
        logger.info("User settings received")
    return user_setting["user_currencies"], user_setting["user_stocks"]
