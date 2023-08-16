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
def getSubtitle(ID):
    try:
        # 동영상의 자막 정보 조회
        transcript_list = YouTubeTranscriptApi.list_transcripts(ID)
        # 한국어 (ko) 자막 가져오기
        korean_transcript = transcript_list.find_transcript(['ko']).fetch()
        captions = [entry['text'] for entry in korean_transcript if '[음악]' not in entry['text'] and '[박수]' not in entry['text']]

    except Exception as e:
        return "0"
    return captions

def searchKeywords(keyword, data_dict):
        
        url = 'https://www.youtube.com/results?search_query={}'.format(keyword)
        driver.get(url)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.yt-spec-button-shape-next--icon-trailing > yt-touch-feedback-shape:nth-child(3) > div:nth-child(1)').click()
        time.sleep(5)

        soup = bs(driver.page_source, 'html.parser')
        for tag in soup.find_all('div', class_='style-scope ytd-item-section-renderer'):
            inner_div = tag.find('div', class_='badge badge-style-type-live-now-alternate style-scope ytd-badge-supported-renderer style-scope ytd-badge-supported-renderer')
            if inner_div:
                tag.decompose()
        driver.close()
        
        title = soup.select('a#video-title')
        link = soup.select('a#video-title')
        view = soup.select('a#video-title')

        for i in range(len(link)):
            link_url = link[i].get('href')
            if "shorts" in link_url:
                continue  # shorts가 포함된 링크인 경우 pass
            data_dict['link'].append('{}{}'.format('https://www.youtube.com', link_url))
            data_dict['내용'].append(title[i].text.strip())

            temp = getSubtitle(link_url[len("/watch?v="):].split("&")[0])
            text = ""
            for j in temp:
                text = j + text
            data_dict['상세내용'].append(text)
            data_dict['view'].append(view[i].get('aria-label').split()[-2])
    
        # 빈 열에 '0' 임시 처방
        for key in data_dict:
            if not data_dict[key]:
                data_dict[key] = ["0"] * len(data_dict['view'])
        df = pd.DataFrame(data_dict)
        return df
# ------------------------------------ ↑↑↑ 함수 설정 ↑↑↑ ------------------------------------ #

csv_filename = 'output.csv'

# 빈 딕셔너리 생성
content_total_dict = {'주제': [], '내용': [], '상세내용': [], '주장/검증매체': [], 'label': [], 'link': [], 'view': [], 'upload_date': []}

keyword = ["탄소"]

for i in keyword:
    searchKeywords(i, content_total_dict).to_csv(csv_filename, index=True, index_label='row_data')

print(f"데이터가 {csv_filename} 파일로 저장되었습니다.") 