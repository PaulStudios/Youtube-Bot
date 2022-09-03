import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
import youtube_dl
import pafy


def error(code):
    print("Something went wrong. Error Code :- " + code + ".")
    print("Please seek support from developer with the error code.")

videos = []

def loadlist():
    global videos
    with open("List.json", "r") as file:
        data = json.loads(file.read())
    list = []
    for i in range(len(data)):
        v = data[str(i)][1]
        list.append(v)
    print(list)
    videos = list
    return list

loadlist()

while(True):
    for i in videos:
        try:
            driver = webdriver.Chrome("chromedriver.exe")
        except selenium.common.exceptions.SessionNotCreatedException:
            print("Please install Chrome version 105.")
        except Exception as e:
            error("ER12 - [" + str(e) + "]")
        try:
            video = pafy.new(i)
            print("Current Video : " + video.title) #fix dislike_count error from stackoverflow
            print("Likes : " + str(video.likes))
            print("Views : " + str(video.viewcount))
            print(" ")
            driver.get("https://www.youtube.com/watch?v=" + i)
            time.sleep(2)
            #play_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Play (k)']")))
            #play_btn.click()
            time.sleep(200)
            driver.close()
        except youtube_dl.utils.ExtractorError as e:
            error("ER19 - [" + str(e) + "]")
        except youtube_dl.utils.DownloadError as e:
            error("ER19 - [" + str(e) + "]")
        except OSError as e:
            pass
            #error("ER19 - [" + str(e) + "]")
        except selenium.common.exceptions.TimeoutException as e:
            error("ER19 - [" + str(e) + "]")

