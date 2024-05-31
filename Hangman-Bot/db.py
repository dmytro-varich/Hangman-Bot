import sqlite3 as sq
from datetime import datetime
from math import ceil

async def db_start():
    global db, cur
    db = sq.connect('new.db')
    cur = db.cursor()
    # cur.execute("DROP TABLE IF EXISTS profile")
    cur.execute("""CREATE TABLE IF NOT EXISTS profile(
                    user_id TEXT PRIMARY KEY, 
                    secret TEXT, 
                    count INTEGER, 
                    letters_guessed TEXT, 
                    language TEXT, 
                    start_time TEXT, 
                    topic TEXT,
                    topic_id TEXT,  
                    points INTEGER, 
                    option TEXT,
                    total_points INTEGER, 
                    daily_word TEXT, 
                    mode TEXT)
                """)

    cur.execute("""CREATE TABLE IF NOT EXISTS statistics (
                    statistics_id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    tag_name TEXT,
                    secret TEXT,
                    count INTEGER,
                    time TEXT,
                    topic TEXT,
                    points INTEGER,
                    FOREIGN KEY (user_id) REFERENCES profile (user_id),
                    FOREIGN KEY (secret) REFERENCES profile (secret),
                    FOREIGN KEY (time) REFERENCES profile (time),
                    FOREIGN KEY (topic) REFERENCES profile (topic)
                )""")

    db.commit()


async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, '', 0, '', '', '', '', '', 0, '', 0, '', ''))
    db.commit()


async def create_profile_to_play(user_id, secret):
    cur.execute("UPDATE profile SET secret = '{}', count = '{}', letters_guessed = '{}' WHERE "
                "user_id == '{}'".format(secret, 8, '', user_id))
    db.commit()


async def create_statistics(user_id, tag_name, secret, count, time, topic, points):
    cur.execute("INSERT INTO statistics (user_id, tag_name, secret, count, time, topic, points) VALUES (?, ?, ?, ?, "
                "?, ?, ?)",
                (user_id, tag_name, secret, count, time, topic, points))
    db.commit()

    cur.execute("SELECT COUNT(*) FROM statistics WHERE user_id = ?", (user_id,))
    record_count = cur.fetchone()[0]

    if record_count > 5:
        cur.execute("DELETE FROM statistics WHERE statistics_id IN (SELECT statistics_id FROM statistics WHERE "
                    "user_id = ? ORDER BY points ASC LIMIT 1)",
                    (user_id,))
        db.commit()


async def show_statistics(user_id):
    cur.execute("SELECT secret, count, time, topic, points FROM statistics WHERE user_id = ? ORDER BY points DESC",
                (user_id,))
    user_statistics = cur.fetchall()
    return user_statistics


async def add_topic(user_id, topic, topic_id):
    cur.execute("UPDATE profile SET topic = ?, topic_id=? WHERE user_id = ?", (topic, topic_id, user_id))
    db.commit()


async def add_mode(user_id, mode):
    cur.execute("UPDATE profile SET mode = ? WHERE user_id = ?", (mode, user_id))
    db.commit()


async def total_points(user_id, points_to_add):
    cur.execute("UPDATE profile SET points = points + ? WHERE user_id = ?", (points_to_add, user_id))
    db.commit()


async def add_total_points(user_id, total_points_for_user):
    cur.execute("UPDATE profile SET total_points = total_points + ? WHERE user_id = ?", (total_points_for_user, user_id))
    db.commit()


async def rating_show():
    cur.execute("SELECT user_id, total_points FROM profile GROUP BY user_id")
    best_records = cur.fetchall()
    best_records.sort(key=lambda x: x[1], reverse=True)
    top_users = best_records[:50]
    return top_users


async def update_daily(user_id, data):
    cur.execute("UPDATE profile SET option = ? WHERE user_id = ?", (data, user_id))
    db.commit()


async def get_users_with_daily_option():
    cur.execute("SELECT user_id FROM profile WHERE option = ?", ('Yes',))
    users = cur.fetchall()
    user_ids = [user[0] for user in users]
    return user_ids


async def add_daily_word(daily_word):
    cur.execute("UPDATE profile SET daily_word = '{}' WHERE option == '{}'".format(daily_word, 'Yes'))
    db.commit()


async def update_points(user_id, points):
    cur.execute("UPDATE profile SET points = ? WHERE user_id = ?", (points, user_id))
    db.commit()


async def update_start_time(user_id, start_time):
    cur.execute("UPDATE profile SET start_time = ? WHERE user_id = ?", (start_time, user_id))
    db.commit()


def get_data(user_id, index):
    result = cur.execute(
        'SELECT user_id, secret, count, letters_guessed, language, start_time, topic, topic_id, points, total_points, daily_word, mode FROM profile WHERE user_id = ?',
        (user_id,)).fetchall()
    if result:
        return result[0][index]
    return None


def get_time(user_id):
    start_time_str = get_data(user_id, 5)
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    elapsed_time = datetime.now() - start_time
    seconds = elapsed_time.total_seconds()
    return ceil(seconds)


async def change_count(user_id, count):
    cur.execute("UPDATE profile SET count = '{}' WHERE user_id == '{}'".format(count, user_id))
    db.commit()


async def change_letters_guessed(user_id, letters_guessed):
    cur.execute("UPDATE profile SET letters_guessed = ? WHERE user_id = ?", (letters_guessed, user_id))
    db.commit()

async def change_language(user_id, language):
    cur.execute("UPDATE profile SET language = '{}' WHERE user_id == '{}'".format(language, user_id))
    db.commit()


async def delete_row(user_id):
    cur.execute("DELETE FROM profile WHERE user_id='{}'".format(user_id))
    db.commit()
