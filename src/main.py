from src.services import simple_search, search_phone_numbers, calculate_increased_cashback
from src.utils import get_transactions_from_excel
from src.views import main_page

if __name__ == "__main__":
    df = get_transactions_from_excel(r"C:\Users\anisa\PycharmProjects\Course-Transaction-Analysis-\data\operations.xlsx")
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
