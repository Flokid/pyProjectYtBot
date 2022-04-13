import asyncio
import datetime
import os

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from pytube import YouTube

import letter
from Download_with_different_resolutions import download_vid, download_vid_only_audio
from Info import Info
from atribute_getter import AttGetter as ag
from db_worker import DBWorker as dbworker
from keyboard import menu, back, make_keyboards_with_video_settings, again_video, again_channel, help, \
    make_keyboards_with_channel_video
from parsing_yt_channel import parse_channel

# ссылка на бота -    https://t.me/Sown_bot

bot = Bot(token='5271444163:AAF-RK_WlKJLaPfC_iZfHPpPi8HPQZNpdak')
dp = Dispatcher(bot, storage=MemoryStorage())

db = dbworker(bot)
buff_list = []
dt_now = datetime.datetime.now().replace(microsecond=0)
loop = asyncio.get_event_loop()


@dp.message_handler(commands=['start'])
async def get_text_messages(message):
    await bot.send_message(message.from_user.id, letter.Menu.start_hi)
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    db.db_table_users(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username, date=dt_now)


@dp.message_handler(commands=['download'])
async def start_download(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=letter.Menu.start_message,
                           reply_markup=menu())


@dp.message_handler(commands=['help'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=letter.Menu.helps)


@dp.message_handler(text='Скачать все видео с канала ютуба')
async def save_video(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=letter.Menu.get_url_channel, reply_markup=back())
    await Info.channel.set()


@dp.message_handler(text='Скачать видео с ютуба')
async def save_video(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=letter.Menu.get_url, reply_markup=back())
    await Info.video.set()


@dp.message_handler(text='Вернуться в главное меню')
async def save_video(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=letter.Menu.get_back, reply_markup=help())


@dp.message_handler(text='Ещё видео')
async def save_video(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=letter.Menu.get_url, reply_markup=back())
    await Info.video.set()


@dp.message_handler(text='Ещё канал')
async def save_video(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=letter.Menu.get_url_channel, reply_markup=back())
    await Info.channel.set()


@dp.message_handler(state=Info.channel, content_types=types.ContentTypes.TEXT)
async def edit_name(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await bot.send_message(chat_id=message.chat.id, text=letter.Menu.helps)
        await state.finish()
    else:
        if message.text.startswith(letter.Menu.start_with):
            try:

                channel_url = message.text
                await loop.create_task(download_channel_video(channel_url))
                if message.from_user.id == '/download':
                    start_download()
                # th = Thread(target=download_channel_video(channel_url))
                # th.start()
                #
                # print('next')

                # await parse_channel(channel_url)
                # f = open("video_channel.txt")
                # with open("video_channel.txt") as file:
                #     for line in file:
                #         save_path = "C:/Users/Floki/Desktop/pyProject"
                #         link = str(line)
                #         yt = YouTube(link)
                #         streams = yt.streams
                #         video_best = streams.order_by('resolution').asc().first()
                #
                #         try:
                #             video_best.download(save_path)
                #             vv = video_best.title
                #             res = video_best.subtype
                #             buff_list.append(str(vv + "." + res))
                #             # print(buff_list)
                #             # print(len(buff_list))
                #         except:
                #             print("error")

                await bot.send_message(chat_id=message.chat.id,
                                       text="Видео загружены!",
                                       reply_markup=make_keyboards_with_channel_video())
                await state.finish()
            except OSError:
                await bot.send_message(chat_id=message.chat.id,
                                       text=letter.Errors.critical_error,
                                       reply_markup=back(), parse_mode="MarkdownV2")
                await state.finish()
            except ValueError:
                await bot.send_message(chat_id=message.chat.id,
                                       text=letter.Errors.critical_error,
                                       reply_markup=back(), parse_mode="MarkdownV2")
                await state.finish()

        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text=letter.Errors.url_error,
                                   reply_markup=back(), parse_mode="MarkdownV2")
            await state.finish()


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
                db.db_table_video(user_id=us_id, name=ag.get_author(video_url), title=ag.get_title(video_url),
                                  video=video_url,
                                  date=dt_now)
                await bot.send_message(chat_id=message.chat.id,
                                       text=f'Название видео: {ag.get_title(video_url)}\n'
                                            f'Автор: {ag.get_author(video_url)}\n\nВыберите качество загрузки:',
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
        video_url = ag.get_url(call.data)
        download_link = ag.get_download_url_with_audio(video_url)
        file_name = download_vid(download_link, ag.get_title(video_url))
        with open(file_name, "rb") as file:
            spot = await bot.send_document(chat_id, file)
            print(spot.message_id)
            db.db_table_file_id(file_id=spot.message_id, date=dt_now)
            os.remove(file_name)
            await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_video(download_link),
                                   reply_markup=again_video())
    elif call.data.startswith('best_video'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        video_url = ag.get_url(call.data)
        download_link = ag.get_download_url_best_video(video_url)
        file_name = download_vid(download_link, ag.get_title(video_url))
        with open(file_name, "rb") as file:
            spot = await bot.send_document(chat_id, file)
            print(spot.message_id)
            os.remove(file_name)
            await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_less_audio(download_link),
                                   reply_markup=again_video())
    elif call.data.startswith('best_audio_mp3'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        video_url = ag.get_url(call.data)
        download_link = ag.get_download_url_best_audio(video_url)
        res = ".mp3"
        file_name = download_vid_only_audio(download_link, ag.get_title(video_url), res)
        with open(file_name, "rb") as file:
            spot = await bot.send_document(chat_id, file)
            print(spot.message_id)
            os.remove(file_name)
            await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_audio(download_link),
                                   reply_markup=again_video())
    elif call.data.startswith('best_audio_waf'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        video_url = ag.get_url(call.data)
        download_link = ag.get_download_url_best_audio(video_url)
        res = ".waf"
        file_name = download_vid_only_audio(download_link, ag.get_title(video_url), res)
        with open(file_name, "rb") as file:
            spot = await bot.send_document(chat_id, file)
            print(spot.message_id)
            os.remove(file_name)
            await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_audio(download_link),
                                   reply_markup=again_video())
    elif call.data.startswith('best_audio_aif'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        video_url = ag.get_url(call.data)
        download_link = ag.get_download_url_best_audio(video_url)
        res = ".aif"
        file_name = download_vid_only_audio(download_link, ag.get_title(video_url), res)
        with open(file_name, "rb") as file:
            spot = await bot.send_document(chat_id, file)
            print(spot.message_id)
            os.remove(file_name)
            await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_audio(download_link),
                                   reply_markup=again_video())
    elif call.data.startswith('best_audio_mid'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        video_url = ag.get_url(call.data)
        download_link = ag.get_download_url_best_audio(video_url)
        res = ".mid"
        file_name = download_vid_only_audio(download_link, ag.get_title(video_url), res)
        with open(file_name, "rb") as file:
            spot = await bot.send_document(chat_id, file)
            print(spot.message_id)
            os.remove(file_name)
            await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_audio(download_link),
                                   reply_markup=again_video())
    elif call.data.startswith('all_video_channel'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        for i in range(len(buff_list)):

            list = ["?", "`", ",", "/", "'", "*", ".", "%", "#"]
            file_name = buff_list[i]
            file_res = file_name.split(".")[-1]

            for element in list:
                file_name = file_name.replace(element, "")
            file_name = file_name.replace(file_res, "." + file_res)
            print(file_name)

            with open(file_name, "rb") as file:
                spot = await bot.send_document(chat_id, file)
                print(spot.message_id)
                os.remove(file_name)
                await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back_all_video,
                                       reply_markup=again_channel())


    elif call.data == 'cancel':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(chat_id=chat_id, text=letter.Menu.get_back, reply_markup=help())


async def download_channel_video(channel_url):
    await parse_channel(channel_url)
    f = open("video_channel.txt")
    with open("video_channel.txt") as file:
        for line in file:
            await asyncio.sleep(0.1)
            save_path = "C:/Users/Floki/Desktop/pyProject"
            link = str(line)
            yt = YouTube(link)
            streams = yt.streams
            video_best = streams.order_by('resolution').asc().first()
            try:
                video_best.download(save_path)
                vv = video_best.title
                res = video_best.subtype
                buff_list.append(str(vv + "." + res))
                # print(buff_list)
                # print(len(buff_list))
            except:
                print("error")
    print('Конец скачивания')
    return


if __name__ == "__main__":
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)
    loop.run_forever()
