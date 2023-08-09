from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import time
import re
import os

# ------------------------------------ ↓↓↓ Selenium Firefox 설정 ↓↓↓ ------------------------------------ #
# headless mode 사용
options = webdriver.FirefoxOptions()
options.headless = True

# binary 경로
firefox_binary_path = "/usr/bin/firefox-esr"
options.binary_location = firefox_binary_path

# display port 설정
display_port = os.environ.get("DISPLAY_PORT", "99")
display = f":{display_port}"
os.environ["DISPLAY"] = display

# Xvfb 서버 시작
xvfb_cmd = f"Xvfb {display} -screen 0 1920x1080x24 -nolisten tcp &"
os.system(xvfb_cmd)

# 파이어폭스 드라이브 시작
driver = webdriver.Firefox(options=options)
# ------------------------------------ ↑↑↑ Selenium Firefox 설정 ↑↑↑ ------------------------------------ #



# ------------------------------------ ↓↓↓ 함수 설정 ↓↓↓ ------------------------------------ #


def getUrlList(ID):
        url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'.format(ID)
        driver.get(url)
        time.sleep(1)

        soup = bs(driver.page_source, 'html.parser')
        driver.close()
        
        title = soup.select('a.info') # 네이버뉴스 버튼
        print(title)

# ------------------------------------ ↑↑↑ 함수 설정 ↑↑↑ ------------------------------------ #

ID = '새만금'
getUrlList(ID)