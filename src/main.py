from src.reports import spending_by_category
from src.services import calculate_increased_cashback, search_phone_numbers, simple_search
from src.utils import get_transactions_from_excel
from src.views import main_page

if __name__ == "__main__":
    df = get_transactions_from_excel()
    transactions = df.to_dict(orient="records")

    # Страница Главная
    print(main_page("2021-09-30 10:30:00"))

    # Категории повышенного кешбека
    increased_cashback = calculate_increased_cashback(transactions, year="2020", month="09")
    print("\nАнализ кэшбэка:", increased_cashback)

    # Простой поиск
    search_result = simple_search(transactions, "Такси")
    print("\nПростой поиск:", search_result)

    # Поиск телефонов
    phone_result = search_phone_numbers(transactions)
    print("\nПоиск по телефонам:", phone_result)

    # отчет по тратам в определённой категории
    result_df = spending_by_category(df, category="Супермаркеты", date="2021-12-31")
    print("\nТраты в категории 'Супермаркеты':\n", result_df.head())
