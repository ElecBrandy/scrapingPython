from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from youtube_transcript_api import YouTubeTranscriptApi
from collections import Counter
import pandas as pd
import time
import ast
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
def get_top_n_frequencies(input_list, n):
    frequency_counter = Counter(input_list)  # 각 요소의 빈도수 계산
    top_n_frequencies = frequency_counter.most_common(n)  # 빈도수 상위 n개 선택
    top_n_elements = [element for element, _ in top_n_frequencies]  # 요소만 추출
    return top_n_elements

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

def searchKeywords(keyword, data_dict, num):
        url = 'https://www.youtube.com/results?search_query={}'.format(keyword)
        print(url)
        driver.get(url)
        time.sleep(1)

        # 조회수 내림차순 정렬
        driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/div/ytd-search-header-renderer/div[3]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div').click()
        driver.find_element(By.XPATH, '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-search-filter-options-dialog-renderer/div[2]/ytd-search-filter-group-renderer[5]/ytd-search-filter-renderer[3]/a/div/yt-formatted-string').click()
        time.sleep(1)
        print("조회수 내림차순 정렬 완료")

        while True:
            cnt = 1

            # bs4 파싱
            soup = bs(driver.page_source, 'html.parser')
            print("파싱완료")

            # 라이브 영상 제외하기 -> 라이브 영상은 자막제공 X
            for tag in soup.find_all('div', class_='style-scope ytd-item-section-renderer'):
                inner_div = tag.find('div', class_='badge badge-style-type-live-now-alternate style-scope ytd-badge-supported-renderer style-scope ytd-badge-supported-renderer')
                if inner_div:
                    tag.decompose()
            print("라이브영상 제거 완료")
            
            title = soup.select('a#video-title')
            link = soup.select('a#video-title')
            view = soup.select('a#video-title')
            print("요소 담기 완료")
            
            for i in range(len(link)):
                link_url = link[i].get('href')
                if "shorts" in link_url:
                    continue  # shorts가 포함된 링크인 경우 pass
                data_dict['link'].append('{}{}'.format('https://www.youtube.com', link_url))
                print('{}{}'.format('https://www.youtube.com', link_url))
                data_dict['내용'].append(title[i].text.strip())
                print("     영상제목 : " + title[i].text.strip())
                temp = getSubtitle(link_url[len("/watch?v="):].split("&")[0])
                print("자막 생성 완료")

                # 유튜브 스크립트 text로 변환하기
                text = ""
                for j in temp:
                    text = j + text
                data_dict['상세내용'].append(text)
                data_dict['view'].append(view[i].get('aria-label').split()[-2])

                if num <= cnt:
                    break
                else:    
                    cnt = cnt + 1
                    print(cnt)
            if num >= cnt:
                break
            
            # 끝까지 스크롤
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

# topNum -> 상위 몇개의 키워드를 사용할 것인지
# videoNum -> 키워드로 검색해 몇개 영상의 스크립트를 가져올 것인지
def outCSV(csvColum, topNum, videoNum, data_dict):
    for i in csvColum:
        temp = ast.literal_eval(i)
        keyword_list = get_top_n_frequencies(temp, topNum)
        combine = '%2C+'.join(keyword_list) # 키워드 묶어서 한줄로
        print(combine)
        searchKeywords(combine, data_dict, videoNum)

    # 빈 열에 '0' 임시 처방
    for key in data_dict:
        if not data_dict[key]:
            data_dict[key] = ["0"] * len(data_dict['view'])

    df = pd.DataFrame(data_dict)
    df.to_csv('youtube.csv', index=True, index_label='row_data')
    return True
# ------------------------------------ ↑↑↑ 함수 설정 ↑↑↑ ------------------------------------ #
content_total_dict = {'내용': [], '상세내용': [], '주장/검증매체': [], 'label': [], 'link': [], 'view': []}
df_snu = pd.read_csv('./csv/SNU.csv', encoding='euc-kr')
outCSV(df_snu['상세내용'], 3, 3, content_total_dict)

print(f"데이터 저장완료~")
