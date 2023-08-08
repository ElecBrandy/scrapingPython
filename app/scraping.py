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

# tabulate 한글깨짐 방지
# tabulate.WIDE_CHARS_MODE = False

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

    # korean_transcript 변수에 한국어 자막 내용 저장
    print(korean_transcript)

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

    # 쇼츠 정보 삭제
    soup_source.find('ytd-reel-shelf-renderer', class_='style-scope ytd-item-section-renderer').decompose()
    
    # 콘텐츠 모든 정보
    content_total = soup_source.find_all(class_ = 'yt-simple-endpoint style-scope ytd-video-renderer')
    # 콘텐츠 제목만 추출
    content_total_title = list(map(lambda data: data.get_text().replace("\n", ""), content_total))
    # 콘텐츠 링크만 추출
    content_total_link = list(map(lambda data: "https://youtube.com" + data["href"], content_total))
    # 조회수 및 업로드 날짜 추가
    content_record_src = soup_source.find_all(class_ = 'inline-metadata-item style-scope ytd-video-meta-block')
    
    content_view_cnt = [record.get_text() for record in content_record_sr[::2]]
    content_upload_date = [record.get_text() for record in content_record_src[1::2]]

    # 데이터 딕셔너리에 추가
    for title, link, view, upload_date in zip(content_total_title, content_total_link, content_view_cnt, content_upload_date):
        if "https://youtube.com/shorts" in link:
            continue  # shorts 링크인 경우 건너뜀
        data_dict['title'].append(title)
        data_dict['link'].append(link)
        data_dict['view'].append(view)
        data_dict['upload_date'].append(upload_date)

    df = pd.DataFrame(data_dict)
    return df

# ------------------------------------ ↑↑↑ 함수 설정 ↑↑↑ ------------------------------------ #

# 빈 딕셔너리 생성
content_total_dict = {'title': [], 'link': [], 'view': [], 'upload_date': []}

t = "아이폰"
tt = searchKeywords(t, content_total_dict)
# print(tabulate(tt, headers='keys', tablefmt='fancy_outline'))
# CSV 파일로 저장

csv_filename = 'output.csv'
tt.to_csv(csv_filename, index=True, index_label='row_data')

print(f"데이터가 {csv_filename} 파일로 저장되었습니다.")

# # 4. 스크립트만 추출하기
# elements = driver.find_elements(By.CSS_SELECTOR, "html body ytd-app div#content.style-scope.ytd-app ytd-page-manager#page-manager.style-scope.ytd-app ytd-watch-flexy.style-scope.ytd-page-manager.hide-skeleton div#columns.style-scope.ytd-watch-flexy div#secondary.style-scope.ytd-watch-flexy div#secondary-inner.style-scope.ytd-watch-flexy div#panels.style-scope.ytd-watch-flexy ytd-engagement-panel-section-list-renderer.style-scope.ytd-watch-flexy")
# try:
#     print("클릭완료!")
# except:
#     print("실패!")
# finally:
#     driver.quit()
# # 찾은 요소들의 텍스트 출력
# for element in elements:

# elements = driver.find_elements(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
# print(elements)


# Close the browserdriver.quit()