import logging
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
rlt_file_path = os.path.join(current_dir, "../logs/views.log")
abs_file_path = os.path.abspath(rlt_file_path)

logger = logging.getLogger("views")
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

def main_page(date=None) -> dict:
    """Функция отображения главной страницы, объединяющая несколько вспомогательных функций"""
    pass
