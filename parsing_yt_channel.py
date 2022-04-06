import os
import time

from bs4 import BeautifulSoup as BS
from selenium import webdriver


def parse_channel(URL):
    # URL = "https://www.youtube.com/channel/UCtBi_KbB3eX72-UJ6gY6LEA/videos"
    driver = webdriver.Chrome()
    driver.get(URL)
    if os.path.exists("video_channel.txt"):
        os.remove("video_channel.txt")
    f = open("video_channel.txt", "x")
    time.sleep(3)
    html = driver.page_source
    # print(html)
    soup = BS(html, "html.parser")
    videos = soup.find_all("ytd-grid-video-renderer", {"class": "style-scope ytd-grid-renderer"})
    for video in videos:
        a = video.find("a", {"id": "video-title"})
        # name = a.get("title")
        link = " https://www.youtube.com/" + a.get("href")
        # print(link)
        with open("video_channel.txt", "a", encoding="utf-8") as files:
            files.write(link + "\n")
