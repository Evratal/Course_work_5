
from random import sample

from src.dbcreate import DBcreate
from src.dbmanager import DBManager
from src.hh import HH

def user_interaction(hh_api):
    #Флаг, для контроля заполнения таблицы (делает обязательным пункт 1)
    flag = False

    while True:
        print("\nДоступные команды:")
        print("1. Подбор 10 работодателей с соответствующими вакансиями по запросу")
        print("2. Получить список всех компаний и количество вакансий у каждой компании.")
        print("3. Получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию")
        print("4. Получить среднюю зарплату по вакансиям")
        print("5. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям")
        print("6. Получить список всех вакансий по поисковому запросу")
        print("7. Выход")

        choice = input("Выберите команду (1-7): ")

        # Создаём класс для работы с таблицей
        manager = DBManager()


        if choice == '1':
            # Получаем список работодателей, выбираем 10 случайных компаний, создаём таблицу компаний,
            # после чего получаем вакансии от каждой компании и создаём соответствующую таблицу.

            keyword = input("Введите поисковый запрос: ")
            employers = hh_api.load_employers(keyword)


            if employers is not None and len(employers) > 10:
                print(f"Найдены работодатели по запросу '{keyword}':")
                #Создаем список из 10 случайных компаний
                new_list_employers = sample(employers,10)

                #Перевод флаг в значение True
                flag = True

                #Создаём таблицу компаний и вакансий
                new_tables = DBcreate()
                new_tables.create_table_employers()
                new_tables.create_table_vacancies()

                #Получаем вакансии от каждой компании и заполняем соответствующие таблицы
                hh_vacancies = HH()
                hh_vacancies.connect()

                for employer in new_list_employers:
                    new_tables.add_new_employer(employer)
                    new_vacancies = hh_vacancies.load_vacancies("",employer['id'])
                    for vacancy in new_vacancies:
                        new_tables.add_new_vacancy(vacancy)

            else:
                print("Вакансии не найдены.")


        elif choice == '2':

            if flag:
                manager.get_companies_and_vacancies_count()
            else:
                print("Сначала выберите пункт 1, для получения данных")


        elif choice == '3':

            if flag:
                manager.get_all_vacancies()
            else:
                print("Сначала выберите пункт 1, для получения данных")

        elif choice == '4':

            if flag:
                print("Средняя зарплата по всем имеющимися вакансиям")
                manager.get_avg_salary()
            else:
                print("Сначала выберите пункт 1, для получения данных")

        elif choice == '5':

            if flag:
                print("Список вакансий с зарплатой выше средней")
                manager.get_vacancies_with_higher_salary()
            else:
                print("Сначала выберите пункт 1, для получения данных")

        elif choice == '6':

            if flag:
                user_keyword = input("Введите поисковый запрос: ")
                print(f"Результат поиска по запросу: {user_keyword}")
                manager.get_vacancies_with_keyword(user_keyword)
            else:
                print("Сначала выберите пункт 1, для получения данных")

        elif choice == '7':
            print("Выход из программы.")
            break
        #
        else:
            print("Некорректный ввод. Пожалуйста, выберите команду от 1 до 7.")