import psycopg2


class DBManager():

    def printing_result (self,results):
        if results:
            for row in results:
                print(row)
        else:
            print("Результаты не найдены.")

        #получает список всех компаний и количество вакансий у каждой компании.
    def get_companies_and_vacancies_count(self):
        with psycopg2.connect(host='localhost',
                                database='analysis',
                                user='postgres',
                                password='azerty1998') as conn:

            with conn.cursor() as cur:
                cur.execute("""
                          SELECT employer_name, count(*) as cnt 
                          FROM hh_employers 
                          INNER join hh_vacancies USING(ID_employer)
                            GROUP BY employer_name
                            ORDER BY cnt
                          """)

                conn.commit()

                results = cur.fetchall()
                self.printing_result(results)



#получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
    def get_all_vacancies(self):
        with psycopg2.connect(host='localhost',
                                database='analysis',
                                user='postgres',
                                password='azerty1998') as conn:

            with conn.cursor() as cur:
                cur.execute("""
                          SELECT employer_name,vacancy_name,salary,vacancy_url
                          FROM hh_employers 
                          INNER join hh_vacancies USING(ID_employer)
                          GROUP BY employer_name,vacancy_name,salary,vacancy_url
                          """)

                conn.commit()

                results = cur.fetchall()
                self.printing_result(results)


# получает среднюю зарплату по вакансиям
    def get_avg_salary(self):
        with psycopg2.connect(host='localhost',
                                database='analysis',
                                user='postgres',
                                password='azerty1998') as conn:

            with conn.cursor() as cur:
                conn = psycopg2.connect(host='localhost',
                                        database='analysis',
                                        user='postgres',
                                        password='azerty1998')

                # create cursor
                cur = conn.cursor()
                cur.execute("""
                          SELECT CAST(AVG(salary) as decimal(10, 2)) as avg_salary
                            FROM hh_vacancies; 
                          """)

                conn.commit()

                results = cur.fetchall()
                self.printing_result(results)

# получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
    def get_vacancies_with_higher_salary(self):
        with psycopg2.connect(host='localhost',
                                database='analysis',
                                user='postgres',
                                password='azerty1998') as conn:

            with conn.cursor() as cur:
                cur.execute("""
                          SELECT vacancy_name,salary,vacancy_url
                          FROM hh_vacancies
                          WHERE salary > (SELECT AVG(salary) AS avg_salary FROM hh_vacancies)
                          ORDER BY salary DESC
                          """)

                conn.commit()

                results = cur.fetchall()
                self.printing_result(results)


    #Получает список вакансий на основании поиска по слову
    def get_vacancies_with_keyword(self,keyword):
        with psycopg2.connect(host='localhost',
                                database='analysis',
                                user='postgres',
                                password='azerty1998') as conn:

            with conn.cursor() as cur:
                cur.execute(f"""
                                      SELECT * FROM hh_vacancies 
                                      WHERE requirement LIKE '%{keyword}%' OR task LIKE '%{keyword}%';
                                      """)

                conn.commit()

                results = cur.fetchall()
                self.printing_result(results)
