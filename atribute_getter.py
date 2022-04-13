import pafy


class AttGetter():
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
