from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
from tabulate import tabulate
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

    # 동영상의 자막 정보 조회
    transcript_list = YouTubeTranscriptApi.list_transcripts(ID)

    # 한국어 (ko) 자막 가져오기
    korean_transcript = transcript_list.find_transcript(['ko']).fetch()

    return korean_transcript

def searchKeywords(keyword, data_dict):
    # 키워드 공백 처리 + url 생성
    text = keyword.replace(' ', '+')
    url = "https://www.youtube.com/results?search_query=" + text
    print("현재 사이트 url : %s", url)

    # url 접근 + 딜레이(3)
    driver.get(url)
    time.sleep(3)
    # 페이지 소스 추출 : selenium으로 html 수집, bs4로 파싱
    html_source = driver.page_source
    soup_source = BeautifulSoup(html_source, 'html.parser')

    # 콘텐츠 모든 정보
    content_total = soup.find_all('a', id='video-title')
    
    # # Youtube 쇼츠 정보 삭제
    # soup_source.find('ytd-reel-shelf-renderer').decompose()

    # 콘텐츠 제목만 추출
    # content_total_title = list(map(lambda data: data.get_text().replace("\n", ""), content_total))
    content_total_title = list(soup.find('a', id='video-title').text)
    # 콘텐츠 링크만 추출
    content_total_link = list(map(lambda data: "https://youtube.com" + data["href"], content_total))
    # 조회수 및 업로드 날짜 추가
    content_record_src = soup_source.find_all(class_ = 'inline-metadata-item style-scope ytd-video-meta-block')
    
    content_view_cnt = [record.get_text() for record in content_record_src[::2]]
    content_upload_date = [record.get_text() for record in content_record_src[1::2]]

    # 데이터 딕셔너리에 추가
    for title, link, view, upload_date in zip(content_total_title, content_total_link, content_view_cnt, content_upload_date):
        data_dict['내용'].append(title)
        data_dict['link'].append(link)
        data_dict['view'].append(view)
        data_dict['upload_date'].append(upload_date)
    
    # for link in data_dict['link']:
    #     ID = link[28:39]
    #     result = getSubtitle(ID)  # a 함수 호출
    #     data_dict['상세내용'].append(result)

    # 빈 열에 '0' 임시 처방    
    for key in data_dict:
        if not data_dict[key]:
            data_dict[key] = ["0"] * len(data_dict['upload_date'])
    df = pd.DataFrame(data_dict)
    return df
# ------------------------------------ ↑↑↑ 함수 설정 ↑↑↑ ------------------------------------ #

# 빈 딕셔너리 생성
print("빈 딕셔너리 생성")
content_total_dict = {'주제': [], '내용': [], '상세내용': [], '주장/검증매체': [], 'label': [], 'link': [], 'view': [], 'upload_date': []}

print("주제설정")
t = "아이폰"

tt = searchKeywords(t, content_total_dict)
# print(tabulate(tt, headers='keys', tablefmt='fancy_outline'))
# CSV 파일로 저장

csv_filename = 'output.csv'
tt.to_csv(csv_filename, index=True, index_label='row_data')

print(f"데이터가 {csv_filename} 파일로 저장되었습니다.")

