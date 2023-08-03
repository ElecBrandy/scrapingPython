from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

url = "https://www.youtube.com/watch?v=RZupmCwrwec"

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

# 페이지로 이동
driver.get(url)


# 딜레이 
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/yt-button-shape/button/yt-touch-feedback-shape/div").click()
time.sleep(5)

# # 2. '스크립트 표시'라는 텍스트를 가진 버튼 클릭
driver.find_element(By.CSS_SELECTOR, "html body ytd-app ytd-popup-container.style-scope.ytd-app tp-yt-iron-dropdown.style-scope.ytd-popup-container div#contentWrapper.style-scope.tp-yt-iron-dropdown ytd-menu-popup-renderer.style-scope.ytd-popup-container tp-yt-paper-listbox#items.style-scope.ytd-menu-popup-renderer ytd-menu-service-item-renderer.style-scope.ytd-menu-popup-renderer").click()

# file = open("test.txt", "w")
print(driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/yt-button-shape/button/yt-touch-feedback-shape/div"))
driver.quit()
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