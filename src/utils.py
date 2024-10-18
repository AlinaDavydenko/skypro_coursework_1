# Helper functions required for the Home page function to work
import datetime
import datetime as dt
import json
import logging
from pathlib import Path
import pandas as pd
import os
import requests
from dotenv import load_dotenv


logger = logging.getLogger("logs")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("..\\logs\\utils.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_data_parameter(data: str) -> datetime.datetime:
    """ Date Conversion Function """
    logger.info(f"Received date string: {data}")
    try:
        data_obj = datetime.datetime.strptime(data, "%d.%m.%Y %H:%M:%S")
        logger.info(f"Converted to object datetime: {data_obj}")
        return data_obj
    except ValueError as e:
        logger.error(f"Date conversion error: {e}")
        raise e


def read_transactions_from_excel(file_path) -> pd.DataFrame:
    """ The function takes a path to a file as input and returns a dataframe """
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


def get_greeting():
    """ Function - greeting """
    hour = dt.datetime.now().hour
    if 4 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 22:
        return "Good evening"
    else:
        return "Good night"
