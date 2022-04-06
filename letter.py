class Menu():
    start_with = 'https://www.youtube.com/watch?v='
    start_message = 'Привет, я помогу тебе скачать видео с YouTube.'

    start_hi = 'Привет! Ваше имя добавленно в базу данных! Напишите или кликните на /help , ' \
               'чтобы увидеть мои комманды!'
    get_url = ' Введи ссылку на видео: '
    get_back = 'Ты вернулся в главное меню.'

    helps = "Данный бот поможет вам скачать видео с платформы ютуб в лучшем качестве." \
            " Загрузить на сервер само видео, загрузить видео без звука - гифку, или, " \
            "загрузить только звуковую дорожку этого видео в расширениях: .mp3; .waf; .aif; .mid.\n\n" \
            "                                           Список команд:\n\n" \
            "/download - запускает Бота.\n\n" \
            "/start - поздаровайся со мной)\n\n\n" \
            "Спасибо, что пользуетесь услугами этого бота!"

    def get_back_video(self):
        return f'Вот ваше видео: ↑'

    def get_back_audio(self):
        return f'Вот ваш звук из видео: ↑'

    def get_back_less_audio(self):
        return f'Вот ваше видео без звука(гифка): ↑'

    def get_different_resolution(self):
        f'Выберите расширение звука: '


class Errors():
    critical_error = 'Ссылка неверная, либо видео не найдено. ' \
                     'Введи ссылку в формате: ```https://www.youtube.com/watch?v=...```'
    url_error = 'Введи ссылку в формате: ```https://www.youtube.com/watch?v=...```'
