from selenium import webdriver
from bs4 import BeautifulSoup as bs
from collections import Counter
import pandas as pd
import time
import os
import ast

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

# 각 키워드 마다 긁어오고 싶은 기사의 갯수 = desired_count
def get_url_list(driver, keyword, desired_count):
    links = []
    new_links = []
    page_number = 0  # 시작 페이지 번호

    while len(links) < desired_count:
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={keyword}&start={page_number}'
        print(url)
        driver.get(url)
        time.sleep(1)
        soup = bs(driver.page_source, 'html.parser')
        link_tags = soup.select('a.info')  # 클래스가 'info'인 모든 <a> 태그 선택
        for link in link_tags:
            if 'naver' in link['href']:
                links.append(link['href'])
                if len(links) >= desired_count:
                    break

        if page_number == 250:
            print("기사 갯수 : ")
            print(len(links))
            for j in links:
                if j not in new_links:
                    new_links.append(j)
            return new_links

        page_number += 10  # 다음 페이지로 이동
    
    
    for j in links:
        if j not in new_links:
            new_links.append(j)
    return new_links


# 기사 정보 추출
def get_news_info(driver, url, data_dict):
    driver.get(url)
    time.sleep(1)
    soup = bs(driver.page_source, 'html.parser')
    title = soup.select("#title_area > span")
    main = soup.select("#dic_area")
    press = soup.select("em.media_end_linked_more_point")
    
    print("기사내용")
    if title != None:
        title_str = title.get_text().strip()
        print(title_str)
    else:
        return
    
    if main != None:
        main_lst = [m.get_text().strip() for m in main]
        main_str = " ".join(main_lst)
    else:
        return
    
    if press != None:
        press_str = press.get_text()
        print(press_str)
    else:
        return
    
    data_dict["주제"].append("경제")
    data_dict["내용"].append(title_str)
    data_dict["상세내용"].append(main_str)
    data_dict["주장/검증매체"].append(press_str)

# topNum -> 상위 몇개의 키워드를 사용할 것인지
# newsNum -> 키워드로 검색해 몇개의 기사를 가져올 것인지
def outCSV(csvColum, topNum, newsNum):
    for i in csvColum:
        temp = ast.literal_eval(i)
        keyword_list = get_top_n_frequencies(temp, topNum)
        print(keyword_list)
        combine = ', '.join(keyword_list) # 키워드 묶어서 한줄로
        print(combine)
        
        url_list = get_url_list(driver, combine, newsNum)
        print('\n')
        print(url_list)
        print('\n')
        for url in url_list:
            get_news_info(driver, url, content_total_dict)

        
    df = pd.DataFrame(content_total_dict)
    df.to_csv('naver.csv', index=True, index_label='row_data')

    return True
# ------------------------------------ ↑↑↑ 함수 설정 ↑↑↑ ------------------------------------ #


df_snu = pd.read_csv('./csv/snu.csv', encoding='utf-8')

content_total_dict = {'주제' : [], '내용': [], '상세내용': [], '주장/검증매체': []}

outCSV(df_snu['상세내용'], 3, 5)

driver.quit()
