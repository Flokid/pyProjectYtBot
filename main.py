import datetime
import os
import sqlite3

import pafy
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

import letter
from Download_with_different_resolutions import download_vid, download_vid_only_audio
from keyboard import menu, back, make_keyboards_with_video_settings, again, help

# ссылка на бота -    https://t.me/Sown_bot

bot = Bot(token='5271444163:AAF-RK_WlKJLaPfC_iZfHPpPi8HPQZNpdak')
dp = Dispatcher(bot, storage=MemoryStorage())

conn = sqlite3.connect("video_database.db")
cursor = conn.cursor()

dt_now = datetime.datetime.now().replace(microsecond=0)


def db_table_users(user_id, user_name, user_surname, username, date):
    cursor.execute('''INSERT INTO users (user_id, user_name, user_surname, username, time) VALUES (?, ?, ?, ?, ?)''',
                   (user_id, user_name, user_surname, username, date))
    conn.commit()


def db_table_video(user_id, name, title, video, date):
    cursor.execute('''INSERT INTO links (user_id, autor, title_name, link, time) VALUES (?, ?, ?, ?, ?)''',
                   (user_id, name, title, video, date))
    conn.commit()


def db_table_file_id(file_id, date):
    cursor.execute('''INSERT INTO file_id (file_id, time) VALUES (?, ?)''',
                   (file_id, date))
    conn.commit()


cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id int, user_name text,
                    user_surname text, username string, time date)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS links
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id int, autor string, title_name string, link string, time date )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS file_id
(id INTEGER PRIMARY KEY  AUTOINCREMENT, file_id int, time date)''')


def get_title(url):
    y_video = pafy.new(url)
    title = y_video.title
    return title


def get_author(url):
    y_video = pafy.new(url)
    author = y_video.author
    return author


def get_url(call):
    url = call.split('|')
    video_url = url[1]
    return video_url


def get_download_url_with_audio(url_video):
    y_video = pafy.new(url_video)
    video = y_video.getbest()
    return video.url_https


def get_download_url_best_video(url_video):
    y_video = pafy.new(url_video)
    video = y_video.getbestvideo()
    return video.url_https


def get_download_url_best_audio(url_video):
    y_video = pafy.new(url_video)
    video = y_video.getbestaudio()
    return video.url_https


class Info(StatesGroup):
    video = State()


@dp.message_handler(commands=['start'])
async def get_text_messages(message):
    if message.text.lower() == '/start':
        await bot.send_message(message.from_user.id, letter.Menu.start_hi)
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    db_table_users(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username, date=dt_now)


@dp.message_handler(commands=['download'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=letter.Menu.start_message,
                           reply_markup=menu())


@dp.message_handler(commands=['help'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=letter.Menu.helps)


@dp.message_handler(text='Скачать видео с ютуба')
async def save_video(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=letter.Menu.get_url, reply_markup=back())
    await Info.video.set()


@dp.message_handler(text='Вернуться в главное меню')
async def save_video(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=letter.Menu.get_back, reply_markup=help())


@dp.message_handler(text='Ещё')
async def save_video(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=letter.Menu.get_url, reply_markup=back())
    await Info.video.set()


@dp.message_handler(state=Info.video, content_types=types.ContentTypes.TEXT)
async def edit_name(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await bot.send_message(chat_id=message.chat.id, text=letter.Menu.helps)
        await state.finish()
    else:
        if message.text.startswith(letter.Menu.start_with):
            try:
                video_url = message.text
                us_id = message.from_user.id
                db_table_video(user_id=us_id, name=get_author(video_url), title=get_title(video_url), video=video_url,
                               date=dt_now)
                await bot.send_message(chat_id=message.chat.id,
                                       text=f'Название видео: {get_title(video_url)}\n'
                                            f'Автор: {get_author(video_url)}\n\nВыберите качество загрузки:',
                                       reply_markup=make_keyboards_with_video_settings(video_url))
                await state.finish()
            except OSError:
                await bot.send_message(chat_id=message.chat.id,
                                       text=letter.Errors.critical_error,
                                       reply_markup=back(), parse_mode="MarkdownV2")
            except ValueError:
                await bot.send_message(chat_id=message.chat.id,
                                       text=letter.Errors.critical_error,
                                       reply_markup=back(), parse_mode="MarkdownV2")

        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text=letter.Errors.url_error,
                                   reply_markup=back(), parse_mode="MarkdownV2")


@dp.callback_query_handler()
async def handler_call(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.from_user.id
    if call.data.startswith('best_with_audio'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        video_url = get_url(call.data)
        download_link = get_download_url_with_audio(video_url)
        file_name = download_vid(download_link, get_title(video_url))
        with open(file_name, "rb") as file:
            spot = await bot.send_document(chat_id, file)
            print(spot.message_id)
            db_table_file_id(file_id=spot.message_id, date=dt_now)
            os.remove(file_name)
            await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_video(download_link),
                                   reply_markup=again())
    elif call.data.startswith('best_video'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        video_url = get_url(call.data)
        download_link = get_download_url_best_video(video_url)
        file_name = download_vid(download_link, get_title(video_url))
        with open(file_name, "rb") as file:
            spot = await bot.send_document(chat_id, file)
            print(spot.message_id)
            os.remove(file_name)
            await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_less_audio(download_link),
                                   reply_markup=again())
    elif call.data.startswith('best_audio_mp3'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        video_url = get_url(call.data)
        download_link = get_download_url_best_audio(video_url)
        res = ".mp3"
        file_name = download_vid_only_audio(download_link, get_title(video_url), res)
        with open(file_name, "rb") as file:
            spot = await bot.send_document(chat_id, file)
            print(spot.message_id)
            os.remove(file_name)
            await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_audio(download_link),
                                   reply_markup=again())
    elif call.data.startswith('best_audio_waf'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        video_url = get_url(call.data)
        download_link = get_download_url_best_audio(video_url)
        res = ".waf"
        file_name = download_vid_only_audio(download_link, get_title(video_url), res)
        with open(file_name, "rb") as file:
            spot = await bot.send_document(chat_id, file)
            print(spot.message_id)
            os.remove(file_name)
            await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_audio(download_link),
                                   reply_markup=again())
    elif call.data.startswith('best_audio_aif'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        video_url = get_url(call.data)
        download_link = get_download_url_best_audio(video_url)
        res = ".aif"
        file_name = download_vid_only_audio(download_link, get_title(video_url), res)
        with open(file_name, "rb") as file:
            spot = await bot.send_document(chat_id, file)
            print(spot.message_id)
            os.remove(file_name)
            await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_audio(download_link),
                                   reply_markup=again())
    elif call.data.startswith('best_audio_mid'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        video_url = get_url(call.data)
        download_link = get_download_url_best_audio(video_url)
        res = ".mid"
        file_name = download_vid_only_audio(download_link, get_title(video_url), res)
        with open(file_name, "rb") as file:
            spot = await bot.send_document(chat_id, file)
            print(spot.message_id)
            os.remove(file_name)
            await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_audio(download_link),
                                   reply_markup=again())

    elif call.data == 'cancel':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back, reply_markup=help())


if __name__ == "__main__":
    # Запускаем бота

    executor.start_polling(dp, skip_updates=True)
