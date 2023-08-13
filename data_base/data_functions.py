import sqlite3 as sq


async def start_db():
    global db, cursor
    db = sq.connect('main_data_base.db')
    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS films "
                   "(film_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, photo TEXT, url TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users "
                   "(id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER UNIQUE, created DATETIME)")
    cursor.execute("CREATE TABLE IF NOT EXISTS started_users "
                   "(id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER UNIQUE, created DATETIME)")
    db.commit()


async def add_user(user_id, added_time):
    try:
        cursor.execute(
            f"INSERT INTO users (telegram_id, created) VALUES('{user_id}', '{added_time}')")
    except Exception as ex:
        print(ex)
    else:
        db.commit()


async def add_film(temp_data):
    cursor.execute(f"INSERT INTO films (title, photo, url) VALUES "
                   f"('{temp_data['title']}', '{temp_data['photo']}', '{temp_data['url']}')")
    db.commit()


async def show_all_films():
    return cursor.execute("SELECT film_id, title FROM films ORDER BY film_id").fetchall()


async def show_film_title(number_of_film):
    return cursor.execute(f"SELECT title FROM films WHERE film_id = {number_of_film}").fetchone()


async def show_film_id(title):
    return cursor.execute(f"SELECT film_id FROM films WHERE title = '{title}'").fetchone()[0]


async def delete_film(title):
    cursor.execute(f"DELETE FROM films WHERE title = '{title}'")
    db.commit()


async def show_last_film_id():
    return cursor.execute("SELECT film_id FROM films ORDER BY film_id DESC LIMIT 1").fetchone()[0]


async def show_film_info(film_id):
    return cursor.execute(f'SELECT * FROM films WHERE film_id = {film_id}').fetchone()


async def show_today_users():
    return cursor.execute("SELECT COUNT(id) FROM users WHERE DATE(created)=DATE('now', 'localtime')").fetchone()


async def show_month_users(day):
    return cursor.execute(f"SELECT COUNT(id) FROM users WHERE DATE(created)>='{day}'").fetchone()


async def show_all_time_users():
    return cursor.execute("SELECT COUNT(id) FROM users").fetchone()


async def add_started_users(user_id, added_time):
    try:
        cursor.execute(
            f"INSERT INTO started_users (telegram_id, created) VALUES('{user_id}', '{added_time}')")
    except Exception as ex:
        print(ex)
    else:
        db.commit()


async def show_today_started_users():
    return cursor.execute("SELECT COUNT(id) FROM started_users WHERE DATE(created)=DATE('now', 'localtime')").fetchone()


async def show_month_started_users(day):
    return cursor.execute(f"SELECT COUNT(id) FROM started_users WHERE DATE(created)>='{day}'").fetchone()


async def show_all_time_started_users():
    return cursor.execute("SELECT COUNT(id) FROM started_users").fetchone()