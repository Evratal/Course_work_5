import psycopg2
import configparser


class DBcreate:

    def __init__(self):

        config = configparser.ConfigParser()
        config.read("config.ini")

        self.conn = None
        try:
            self.conn = psycopg2.connect(
                host=config['database']['host'],
                database=config['database']['database'],
                user=config['database']['user'],
                password=config['database']['password']
            )
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def __del__(self):
        if self.conn:
            self.conn.close()

    def create_table_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS hh_vacancies")
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
            self.conn.commit()

    def create_table_employers(self):
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS hh_employers CASCADE")
            cur.execute('''
                CREATE TABLE IF NOT EXISTS hh_employers (
                    ID_employer integer PRIMARY KEY,
                    employer_name text,
                    url text
                );
            ''')
            self.conn.commit()

    def add_new_vacancy(self, vacancy):
        with self.conn.cursor() as cur:
            salary_value = vacancy["salary"]["from"] if vacancy.get("salary") and "from" in vacancy["salary"] else None
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
            self.conn.commit()

    def add_new_employer(self, employer):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO hh_employers (ID_employer, employer_name, url)
                    VALUES (%s, %s, %s)
                """, (employer["id"], employer["name"], employer["url"]))
                self.conn.commit()
        except psycopg2.Error as e:
            print(f"Ошибка добавления работодателя: {e}")
            self.conn.rollback()  # Откат транзакции в случае ошибки