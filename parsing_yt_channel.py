

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def parse_channel(URL):
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument('--headless')


    driver = webdriver.Chrome(options=options, executable_path='chromedriver.exe')
    driver.get(URL)
    time.sleep(3)
    listings = driver.find_elements(By.XPATH, '//*[@id="thumbnail"and contains (@rel, "null")]')
    with open("video_channel.txt", "w", encoding="utf-8") as files:
        for l in listings:
            if l != "None":
                print(l.get_attribute("href"))
                files.write(str(l.get_attribute("href")) + "\n")

    driver.quit()
    # if os.path.exists("video_channel.txt"):
    #     os.remove("video_channel.txt")
    # f = open("video_channel.txt", "x")
    # # print(mybytes)
    # soup = BS(mybytes, "html.parser")
    # print(soup)
    # videos = soup.find_all("ytd-grid-video-renderer", {"class": "style-scope ytd-grid-renderer"})
    # print(videos)
    # for video in videos:
    #     a = video.find("a", {"id": "video-title"})
    #     # name = a.get("title")
    #     link = " https://www.youtube.com/" + a.get("href")
    #     # print(link)
    #     with open("video_channel.txt", "a", encoding="utf-8") as files:
    #         files.write(link + "\n")
