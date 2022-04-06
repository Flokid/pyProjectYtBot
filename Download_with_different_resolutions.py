import urllib


def download_vid(download_link, title_name):
    name = title_name + '.mp4'
    urllib.request.urlretrieve(download_link, name)
    return name


def download_vid_only_audio(download_link, title_name, resolution):
    name = title_name + '.' + resolution
    urllib.request.urlretrieve(download_link, name)
    return name
