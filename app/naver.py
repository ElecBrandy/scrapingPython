from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
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
# 원하는 keyword와 탐색 범위 pageNumber 입력 시 네이버 기사 링크 리턴
def get_url_list(driver, keyword, page_number):
    links = []
    for i in range(1, page_number + 1):
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={keyword}&start={i}'
        driver.get(url)
        time.sleep(1)
        soup = bs(driver.page_source, 'html.parser')
        link_tags = soup.select('a.info')  # 클래스가 'info'인 모든 <a> 태그 선택
        filtered_links = [link['href'] for j, link in enumerate(link_tags) if 'naver' in link['href']] # 'naver'가 링크에 포함된 경우만 추출
        links.extend(filtered_links)  # 링크 속성(href)값을 리스트로 추가
    return links

# 기사 정보 추출
def get_news_info(driver, url, data_dict):
    driver.get(url)
    time.sleep(1)
    soup = bs(driver.page_source, 'html.parser')
    title = soup.select_one("#title_area > span")
    main = soup.select("#dic_area")
    press = soup.select_one("em.media_end_linked_more_point")
    
    if title:
        title_str = title.get_text().strip()
    else:
        title_str = "No Title"
    
    if main:
        main_lst = [m.get_text().strip() for m in main]
        main_str = " ".join(main_lst)
    else:
        main_str = "No Main Content"
    
    if press:
        press_str = press.get_text()
    else:
        press_str = "No Press Info"
    
    data_dict["내용"].append(title_str)
    data_dict["상세내용"].append(main_str)
    data_dict["주장/검증매체"].append(press_str)
# ------------------------------------ ↑↑↑ 함수 설정 ↑↑↑ ------------------------------------ #

keyword_list = ['새마을', '탄소포집']
    
content_total_dict = {'내용': [], '상세내용': [], '주장/검증매체': []}
    
for keyword in keyword_list:
    url_list = get_url_list(driver, keyword, 10)
    for url in url_list:
        get_news_info(driver, url, content_total_dict)
    
df = pd.DataFrame(content_total_dict)
df.to_csv('naver.csv', index=True, index_label='row_data')

driver.quit()