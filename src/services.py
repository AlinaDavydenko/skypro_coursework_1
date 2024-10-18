import json
import logging
import re


logger = logging.getLogger("logs")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("..\\logs\\services.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_transactions_fizlicam(dict_transaction: list[dict], pattern):
    """The function returns JSON with all transactions that relate to transfers to individuals"""
    logger.info("Function called get_transactions_fizlicam")
    list_transactions_fl = []
    for trans in dict_transaction:
        if "Description" in trans and re.match(pattern, trans["Description"]):
            list_transactions_fl.append(trans)
    logger.info(f"Find {len(list_transactions_fl)} transactions matching the pattern")
    if list_transactions_fl:
        list_transactions_fl_json = json.dumps(list_transactions_fl, ensure_ascii=False)
        logger.info(f"Return JSON со {len(list_transactions_fl)} transactions")
        return list_transactions_fl_json
    else:
        return '[]'
