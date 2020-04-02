import sqlite3


def save_to_db(href, title, salary, company, description):
    conn = sqlite3.connect('data_workua.db')
    c = conn.cursor()
    c.execute('INSERT INTO vacancies VALUES (?, ?, ?, ?, ?)',
              (href, title, salary, company, description))
    conn.commit()
    conn.close()
