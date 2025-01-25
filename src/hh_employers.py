from src.hh import HH
import requests

class HH_emp(HH):
    """
    Класс для работы с API HeadHunter
    """
    def __init__(self):
        super().__init__()
        self.url = 'https://api.hh.ru/employers'

    def load_employers(self, keyword: str):
        """Загружаем вакансии по заданному ключевому слову"""
        self.params['text'] = keyword
        self.params['page'] = 0  # Сброс страницы перед загрузкой
        self.employers = []  # Инициализируем список работодателей

        while self.params['page'] < 20:  # Ограничиваем до 20 страниц
            try:
                response = requests.get(self.url, headers=self.headers, params=self.params)
                response.raise_for_status()  # Поднимаем исключение при ошибках HTTP

                data = response.json()
                employers = data.get('items', [])
                if not employers:  # Если нет вакансий, выходим из цикла
                    break

                # Добавляем компании с открытыми вакансиями
                for emp in employers:
                    if emp.get('open_vacancies', 0) > 0:  # Используем get для безопасной проверки
                        self.employers.append(emp)

                self.params['page'] += 1  # Переходим на следующую страницу

            except requests.exceptions.RequestException as e:
                print(f"Ошибка при получении компаний: {e}")
                break  # Выход при ошибках запроса

        return self.employers  # Возвращаем список работодателей
