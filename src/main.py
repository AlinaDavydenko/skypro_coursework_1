from src.config import file_path, settings_path
from src.reports import spending_by_category
from src.services import get_transactions_fizlicam
from src.utils import get_user_setting, reader_transaction_excel
from src.views import main

if __name__ == "__main__":
    df_transactions = reader_transaction_excel(file_path)
    date = "29.07.2019 22:06:27"
    # Веб - страница
    user_currencies, user_stocks = get_user_setting(settings_path)
    date_json = main(df_transactions, date, user_currencies, user_stocks)

    print(date_json)

    # Сервис
    transactions: list[dict] = df_transactions.to_dict(orient="records")
    result = get_transactions_fizlicam(transactions)
    print(result)

    # Отчёты
    results = spending_by_category(df_transactions, "Каршеринг", "31.12.2021 22:06:27")
    print(results)
