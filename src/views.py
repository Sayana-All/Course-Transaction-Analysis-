import logging
import os

from dotenv import load_dotenv

from src.utils import (converting_data_to_json, currency_rate, filter_operations, get_list_cards, get_top_transactions,
                       get_transactions_from_excel, read_user_settings, stock_prices, user_greeting)

current_dir = os.path.dirname(os.path.abspath(__file__))
rlt_file_path = os.path.join(current_dir, "../logs/views.log")
abs_file_path = os.path.abspath(rlt_file_path)

logger = logging.getLogger("views")
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def main_page(date_str: str) -> str:
    """Главная страница — возвращает JSON по заданной дате"""
    load_dotenv()
    api_key_cr = os.getenv("API_KEY_CURRENCIES")
    api_key_st = os.getenv("API_KEY_STOCKS")
    try:
        df = get_transactions_from_excel()
        operations = filter_operations(df, date_str)
        settings = read_user_settings()
    except Exception as e:
        logger.error(f"Ошибка в main_page: {e}")
        return converting_data_to_json({"error": str(e)})
    else:
        logger.info("Данные для Главной страницы успешно сформированы.")
        return converting_data_to_json(
            {
                "greeting": user_greeting(date_str),
                "cards": get_list_cards(operations),
                "top_transactions": get_top_transactions(operations),
                "currency_rates": currency_rate(api_key_cr, settings.get("user_currencies", []), date_str),
                "stock_prices": stock_prices(api_key_st, settings.get("user_stocks", [])),
            }
        )


if __name__ == "__main__":

    result = main_page("2021-10-20 19:30:00")
    print(type(result))
    print(result)
