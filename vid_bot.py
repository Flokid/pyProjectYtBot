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
from db_worker import DBWorker as db
from keyboard import menu, back, make_keyboards_with_video_settings, again_video, again_channel, help, \
    make_keyboards_with_channel_video
from parsing_yt_channel import parse_channel


class TGBot():
    def start(token):

        bot = Bot(token)
        buff_list = []
        dp = Dispatcher(bot, storage=MemoryStorage())
        executor.start_polling(dp, skip_updates=True)

