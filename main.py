
from src.hh_employers import HH_emp
from src.interface import user_interaction

if __name__ == "__main__":
    hh_api = HH_emp()  # Создаем экземпляр класса HH_emp
    hh_api.connect()  # Подключаемся к API
    user_interaction(hh_api)
