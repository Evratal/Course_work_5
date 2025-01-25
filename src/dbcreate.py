
import psycopg2


class DBcreate():

    def create_table_vacancies(self):

        with psycopg2.connect(host='localhost',
                                database='analysis',
                                user='postgres',
                                password='azerty1998') as conn:

            with conn.cursor() as cur:

                cur.execute("DROP TABLE IF EXISTS hh_vacancies")
                # Создание таблиц для вакансий
                # ID_vacancy-id, первичный ключ ("id")
                # vacancy_name - наименование вакансии ("name")
                # area - место работы ("area")
                # url - url вакансии ("url")
                # employer_id - id работодателя, связанный с соответствующей таблицей ("employer"["id"])
                # requirement - требования к соискателю ("snippet"["requirement"])
                # task - задачи соискателя ("snippet"["responsibility"])
                # schedule - занятость ("schedule")
                # experience - требуемый опыт ("experience")
                cur.execute('''
                CREATE TABLE IF NOT EXISTS hh_vacancies (
                ID_vacancy integer PRIMARY KEY,
                vacancy_name VARCHAR(100),
                area VARCHAR(100),
                vacancy_url VARCHAR(100),
                ID_employer INTEGER,
                requirement TEXT,
                task TEXT,
                schedule VARCHAR(100),
                experience VARCHAR(100),
                salary INT,
                CONSTRAINT fk_employees_department FOREIGN KEY(ID_employer) REFERENCES hh_employers(ID_employer)
                );
                ''')

                conn.commit()


    def create_table_employers(self):

        with psycopg2.connect(host='localhost',
                                database='analysis',
                                user='postgres',
                                password='azerty1998') as conn:

            with conn.cursor() as cur:

                cur.execute("DROP TABLE IF EXISTS hh_employers CASCADE")
                # Создание таблиц компаний
                # ID_employer-id, первичный ключ ("id")
                # employer_name - наименование компании ("name")
                # url - url компании на hh ("alternate_url")


                cur.execute('''
                 CREATE TABLE IF NOT EXISTS hh_employers (
                 ID_employer integer PRIMARY KEY,
                 employer_name VARCHAR(100),
                 url VARCHAR(100));
                ''')

                conn.commit()


    def add_new_vacancy(self,vacancy):

        with psycopg2.connect(host='localhost',
                                database='analysis',
                                user='postgres',
                                password='azerty1998') as conn:

            with conn.cursor() as cur:

                # Проверить, что salary существует и имеет ключ "from"
                if vacancy["salary"] is not None and "from" in vacancy["salary"]:
                    salary_value = vacancy["salary"]["from"]

                    # Выполнить запрос с параметрами
                    cur.execute("""
                        INSERT INTO hh_vacancies (ID_vacancy, vacancy_name, area, vacancy_url, ID_employer, requirement, task, schedule, experience, salary)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        vacancy["id"],
                        vacancy["name"],
                        vacancy["area"]["name"],
                        vacancy["url"],
                        vacancy["employer"]["id"],
                        vacancy["snippet"]["requirement"],
                        vacancy["snippet"]["responsibility"],
                        vacancy["schedule"]["name"],
                        vacancy["experience"]["name"],
                        salary_value
                    ))

                else:
                    salary_value = None
                    cur.execute("""
                                   INSERT INTO hh_vacancies (ID_vacancy, vacancy_name, area, vacancy_url, ID_employer, requirement, task, schedule, experience, salary)
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                               """, (
                        vacancy["id"],
                        vacancy["name"],
                        vacancy["area"]["name"],
                        vacancy["url"],
                        vacancy["employer"]["id"],
                        vacancy["snippet"]["requirement"],
                        vacancy["snippet"]["responsibility"],
                        vacancy["schedule"]["name"],
                        vacancy["experience"]["name"],
                        salary_value
                    ))
                conn.commit()



    def add_new_employer(self, employer):

        with psycopg2.connect(host='localhost',
                                database='analysis',
                                user='postgres',
                                password='azerty1998') as conn:

            with conn.cursor() as cur:
                cur.execute(f"""
                          INSERT INTO hh_employers (ID_employer, employer_name, url)
                          VALUES ('{employer["id"]}',
                                  '{employer["name"]}',
                                  '{employer["url"]}')
                          """
                            )

                conn.commit()

