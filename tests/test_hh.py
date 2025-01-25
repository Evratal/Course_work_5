import pytest
from unittest.mock import patch, MagicMock
from src.parser import Parser  #
from src.hh import HH

@pytest.fixture
def hh():
    return HH()

@patch('requests.get')
def test_connect_success(mock_get, hh):
    mock_get.return_value.status_code = 200

    hh.connect()

    assert mock_get.called
    assert mock_get.call_count == 1

@patch('requests.get')
def test_connect_failure(mock_get, hh):
    mock_get.return_value.status_code = 404

    with pytest.raises(Exception) as excinfo:
        hh.connect()

    assert str(excinfo.value) == "Ошибка подключения к API: 404"


@pytest.fixture
def mock_hh():
    with patch('src.hh.HH') as mock:
        yield mock


def test_load_vacancies_success(mock_hh):

    mock_hh.return_value.load_vacancies.return_value = [
        {'id': 1, 'name': 'Vacancy 1'},
        {'id': 2, 'name': 'Vacancy 2'}
    ]

    vacancies = mock_hh.return_value.load_vacancies("", "some_employer_id")


    assert len(vacancies) == 2  # Проверяем, что количество вакансий равно 2
    assert vacancies[0]['id'] == 1
    assert vacancies[0]['name'] == 'Vacancy 1'
    assert vacancies[1]['id'] == 2
    assert vacancies[1]['name'] == 'Vacancy 2'


@patch('requests.get')
def test_load_vacancies_no_results(mock_get, hh):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'items': [],
        'pages': 0,
    }

    vacancies = hh.load_vacancies('developer', '')

    assert len(vacancies) == 0
    assert hh.params['page'] == 0  # Убедимся, что мы не увеличили страницу

@patch('requests.get')
def test_load_vacancies_error(mock_get, hh):
    mock_get.return_value.status_code = 500

    vacancies = hh.load_vacancies('developer', '')

    assert len(vacancies) == 0
    assert hh.params['page'] == 0  # Страница должна остаться 0 после ошибки