import pytest
from unittest.mock import patch, Mock, MagicMock

from src.hh_employers import HH_emp


class TestLoadEmployers:

    @patch('src.hh_employers.requests.get')  # Замените your_module на реальный путь к вашему модулю
    def test_load_employers_success(self, mock_get):
        # Настройка мок-объекта для возврата успешного ответа
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [
                {'name': 'Employer1', 'open_vacancies': 5},
                {'name': 'Employer2', 'open_vacancies': 0},
                {'name': 'Employer3', 'open_vacancies': 3}
            ]
        }
        mock_get.return_value = mock_response

        employer_loader = HH_emp()
        employer_loader.load_employers('test_keyword')

        assert employer_loader.employers[0]['name'] == 'Employer1'
        assert employer_loader.employers[1]['name'] == 'Employer3'

    @patch('src.hh_employers.requests.get')
    def test_load_employers_error_handling(self, mock_get):
        # Настройка мок-объекта для возврата ошибки
        mock_response = MagicMock()
        mock_response.status_code = 404  # Код ошибки
        mock_get.return_value = mock_response

        employer_loader = HH_emp()
        employer_loader.load_employers('test_keyword')

        # Проверка, что список работодателей остается пустым на ошибках
        assert len(employer_loader.employers) == 0

    @patch('src.hh_employers.requests.get')
    def test_load_employers_empty_response(self, mock_get):
        # Настройка мок-объекта для возврата пустого ответа
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response

        employer_loader = HH_emp()
        employer_loader.load_employers('test_keyword')

        # Проверка, что список работодателей остается пустым в случае отсутствия данных
        assert len(employer_loader.employers) == 0

    @patch('src.hh_employers.requests.get')
    def test_load_employers_no_open_vacancies(self, mock_get):
        # Настройка мок-объекта для возврата данных без открытых вакансий
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [
                {'name': 'Employer1', 'open_vacancies': 0},
                {'name': 'Employer2', 'open_vacancies': 0}
            ]
        }
        mock_get.return_value = mock_response

        employer_loader = HH_emp()
        employer_loader.load_employers('test_keyword')

        # Проверка, что список работодателей остается пустым, если все вакансии закрыты
        assert len(employer_loader.employers) == 0