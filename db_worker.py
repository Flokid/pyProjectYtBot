
import sqlite3

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher


class DBWorker():
    def __init__(self, bot):
        self.dp = Dispatcher(bot, storage=MemoryStorage())

        self.conn = sqlite3.connect("video_database.db")
        self.cursor = self.conn.cursor()



        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id int, user_name text,
                                user_surname text, username string, time date)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS links
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id int, autor string, title_name string, link string, time date )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS file_id
            (id INTEGER PRIMARY KEY  AUTOINCREMENT, file_id int, time date)''')

        self.buff_list = []


    def db_table_users(self, user_id, user_name, user_surname, username, date):
        self.cursor.execute(
            '''INSERT INTO users (user_id, user_name, user_surname, username, time) VALUES (?, ?, ?, ?, ?)''',
            (user_id, user_name, user_surname, username, date))
        self.conn.commit()


    def db_table_video(self, user_id, name, title, video, date):
        self.cursor.execute('''INSERT INTO links (user_id, autor, title_name, link, time) VALUES (?, ?, ?, ?, ?)''',
                            (user_id, name, title, video, date))
        self.conn.commit()


    def db_table_file_id(self, file_id, date):
        self.cursor.execute('''INSERT INTO file_id (file_id, time) VALUES (?, ?)''',
                            (file_id, date))
        self.conn.commit()
