import psycopg2
import configparser

class DBManager():

    def printing_result(self, results):
        if results:
            for row in results:
                print(row)
        else:
            print("Результаты не найдены.")

    def get_connection(self):

        config = configparser.ConfigParser()
        config.read("config.ini")

        return psycopg2.connect(
            host=config['database']['host'],
            database=config['database']['database'],
            user=config['database']['user'],
            password=config['database']['password']
        )

    # получает список всех компаний и количество вакансий у каждой компании
    def get_companies_and_vacancies_count(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT employer_name, COUNT(*) as cnt 
                    FROM hh_employers 
                    INNER JOIN hh_vacancies ON hh_employers.ID_employer = hh_vacancies.ID_employer
                    GROUP BY employer_name
                    ORDER BY cnt
                """)
                results = cur.fetchall()
                self.printing_result(results)

    # получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
    def get_all_vacancies(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT employer_name, vacancy_name, salary, vacancy_url
                    FROM hh_employers 
                    INNER JOIN hh_vacancies ON hh_employers.ID_employer = hh_vacancies.ID_employer
                    ORDER BY vacancy_name
                """)
                results = cur.fetchall()
                self.printing_result(results)

    # получает среднюю зарплату по вакансиям
    def get_avg_salary(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT CAST(AVG(salary) AS decimal(10, 2)) AS avg_salary
                    FROM hh_vacancies
                """)
                results = cur.fetchall()
                self.printing_result(results)

    # получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
    def get_vacancies_with_higher_salary(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT vacancy_name, salary, vacancy_url
                    FROM hh_vacancies
                    WHERE salary > (SELECT AVG(salary) FROM hh_vacancies)
                    ORDER BY salary DESC
                """)
                results = cur.fetchall()
                self.printing_result(results)

    # Получает список вакансий на основании поиска по слову
    def get_vacancies_with_keyword(self, keyword):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM hh_vacancies 
                    WHERE requirement LIKE %s OR task LIKE %s
                """, (f'%{keyword}%', f'%{keyword}%'))
                results = cur.fetchall()
                self.printing_result(results)