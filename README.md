# Course-Transaction-Analysis-
### Курсовая по 3 модулю. Работа с банковскими операциями, файлами и отчетностью.

## Описание
Вы будете разрабатывать приложение для анализа транзакций, которые находятся в Excel-файле. 
Приложение будет генерировать JSON-данные для веб-страниц, формировать Excel-отчеты, а также предоставлять другие сервисы.

## Информация для пользователей
### Данные
Файл с транзакциями пользователя хранится в папке data в формате Excel: [operations.xlsx](data/operations.xlsx)

```Описание данных
- Дата операции — дата, когда произошла транзакция.
- Дата платежа — дата, когда был произведен платеж.
- Номер карты — последние 4 цифры номера карты.
- Статус — статус операции (например, OK, FAILED).
- Сумма операции — сумма транзакции в оригинальной валюте.
- Валюта операции — валюта, в которой была произведена транзакция.
- Сумма платежа — сумма транзакции в валюте счета.
- Валюта платежа — валюта счета.
- Кешбэк — размер полученного кешбэка.
- Категория — категория транзакции.
- MCC — код категории транзакции (соответствует международной классификации).
- Описание — описание транзакции.
- Бонусы (включая кешбэк) — количество полученных бонусов (включая кешбэк).
- Округление на «Инвесткопилку» — сумма, которая была округлена и переведена на «Инвесткопилку».
- Сумма операции с округлением — сумма транзакции, округленная до ближайшего целого числа.
```
### В настоящее время реализовано несколько полезных функций для виджета:
+ в модуле **masks** реализована функция маскировки номера банковской карты и счета пользователя.
+ в модуле **widget** также доступна функция маски номера карты или счета, а также реализована функция форматирования даты и приведения её к виду `"ДД.ММ.ГГГГ"`.
+ в модуле **main** реализована головная функция, отвечающая за общую логику проекта, связывающая остальные функциональности между собой.

_Данные модули прошли проверку тестами на валидность и работоспособность!_


## Логирование
Добавлено сохранение логов в файл для модулей **masks**, **utils** и **read_files**.
Логи сохранены в директории _logs_ в корне проекта.

## Тестирование
В ходе тестирования кода был выполнен ряд проверок и отладки отдельных блоков:

**Модуль masks**  

Функция `get_mask_card_number`:
+ Правильность маскирования номера карты.
+ Параметризованные тесты для проверки работы функции на различных входных форматах номеров карт.
+ Обработка исключения _ValueError_ при случаях, когда номер карты введен некорректно или имеет неправильную длину, нулевое или строчное (буквенное) значение. 


### Общие аспекты тестирования
**Фикстуры.** 
Все фикстуры для тестов модулей проекта перенесены в единый модуль **conftest.py**

**Mock и patch**
Тестирование функции с обращением к API, а также чтение файлов в модуле **read_files** произведено с помощью декоратора patch.

**Покрытие тестами.** 
Все ветви кода и исключения, которые могут быть сгенерированы функциями, тестируются.
Покрытие тестами составляет 93% кода


## Документация
Узнать более подробно о проекте и реализованных функциях можно по следующим ссылкам:
- [функция маски](Homework_9.1.md)
- [виджет](Homework_9.2.md)
- [работа с банковскими операциями (сортировка по ключу и дате)](Homework_10.1.md)
- [генераторы](Homework_11.1.md)
- [тестировка функций](Homework_10.2.md)
- [декораторы](Homework_11.2.md)
- [импорт транзакций из json-файла и конвертация валютных сумм](Homework_12.1.md)
- [логи для masks и utils](Homework_12.2.md)
- [получение данных из csv-файла и excel-файла](Homework_13.1.md)
- [поиск по описанию и основная сборка проекта](Homework_13.2.md)

## Задание
Реализуйте на выбор минимум одну из задач в каждой категории.

```Задачи по категориям:
1. Веб-страницы:
   + Главная
   + События
2. Сервисы:
   + Выгодные категории повышенного кешбэка
   + Инвесткопилка
   + Простой поиск
   + Поиск по телефонным номерам
   + Поиск переводов физическим лицам
3. Отчеты:
   + Траты по категории
   + Траты по дням недели
   + Траты в рабочий/выходной день
```

poetry add --group lint