from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton


def menu():
    download_button = KeyboardButton('Скачать видео с ютуба')
    backup_button = KeyboardButton('Вернуться в главное меню')
    menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu_kb.add(download_button, backup_button)
    return menu_kb


def help():
    help_button = KeyboardButton('/help')
    menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu_kb.add(help_button)
    return menu_kb


def again():
    download_button = KeyboardButton('Ещё')
    backup_button = KeyboardButton('Вернуться в главное меню')
    menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu_kb.add(download_button, backup_button)
    return menu_kb


def back():
    button_back = KeyboardButton('Отмена')
    back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back_keyboard.add(button_back)
    return back_keyboard


def make_keyboards_with_video_settings(url):
    inline_keyboard1 = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Лучшее качество до 1080p(с звуком).', callback_data=f'best_with_audio|{url}')
    button2 = InlineKeyboardButton('Без звука в лучшем качестве(Гифка).', callback_data=f'best_video|{url}')
    button3 = InlineKeyboardButton('Звук в лучшем качестве c расширением звука .MP3.',
                                   callback_data=f'best_audio_mp3|{url}')
    button4 = InlineKeyboardButton('Звук в лучшем качестве c расширением звука .WAF.',
                                   callback_data=f'best_audio_waf|{url}')
    button5 = InlineKeyboardButton('Звук в лучшем качестве c расширением звука .AIF.',
                                   callback_data=f'best_audio_aif|{url}')
    button6 = InlineKeyboardButton('Звук в лучшем качестве c расширением звука .MID.',
                                   callback_data=f'best_audio_mid|{url}')
    button7 = InlineKeyboardButton('Отмена', callback_data=f'cancel')
    inline_keyboard1.add(button)
    inline_keyboard1.add(button2)
    inline_keyboard1.add(button3)
    inline_keyboard1.add(button4)
    inline_keyboard1.add(button5)
    inline_keyboard1.add(button6)
    inline_keyboard1.add(button7)
    return inline_keyboard1
