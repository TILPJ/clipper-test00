"""
chromedriver를 가동시켜 웹페이지를 크롤링하면서
목표가 되는 엘리먼트를 soup 객체로 추출하는 
메서드를 담고 있는 모듈이다.

"""

import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
WAIT = 10 # seconds

def max_window(browser):
    total_width = browser.execute_script("return document.documentElement.offsetWidth")
    total_height = browser.execute_script("return document.documentElement.scrollHeight")
    browser.set_window_size(max(total_width, 1920), total_height)


def get_soup_from_page(url, target_xpath='/html', button_xpath=None, mouse_xpath=None):
    """
    webpage의 url과 chromedriver의 option항목들을 받아 
    webpage <html> 태그 내용물 전체를 soup 객체로 반환하는 메서드.
    target_xpath는 수집하려는 정보가 담긴 minimal 엘리먼트의 xpath.
    (예: 페이지 전체를 soup에 담으려면 '/html'. 그러나 깊히 안잡히는 경우가
    있을 수 있으므로 가급적 범위를 좁혀 정한다.)
    브라우저를 천천히 scrolldown하여 숨겨진 엘리먼트들이 화면에 뜨도록 한다.
    button_xpath는 브라우저 윈도우 확장을 명하는 button 엘리먼트의 xpath 스트링값이다.
    예외 캐치 인디케이터는 "." 이다.
    mouse_xpath는 마우스를 올려놓으면 펼쳐지는 엘리먼트의 xpath 스트링이다.
    예외 캐치 인디케이터는 "~" 이다.

    """

    # heroku 에 배포하기 위해 필요한 옵션들
    options = webdriver.chrome.options.Options()
    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # 이하의 옵션은 부가적인 옵선이다.
    options.add_argument('disable_infobars') # being controlled by automated ... 없애기
    options.add_argument('--remote-debugging-port=9222')
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    
    
    # 웹드라이버 세션을 실행하는 동안 본격적인 스크래이핑 작업을 위해
    # 웹페이지의 모든 DOM들이 들어가도록 soup 인스턴스를 생성한다.
    with webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), options=options) as browser:
        
        browser.implicitly_wait(WAIT)        
        browser.get(url)
        time.sleep(WAIT/2)
        
        max_window(browser)
        
        # Get scroll height
        # last_height = browser.execute_script("return document.body.scrollHeight")       
        last_height = browser.execute_script("return document.documentElement.scrollHeight")
        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

            # Wait to load page
            time.sleep(WAIT/2)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        
        # 펼칠 필요가 있는 경우 버튼을 클릭하여 브라우저를 펼친다.
        if button_xpath:
            try:
                button = browser.find_element_by_xpath(button_xpath)
                button.click()                
            except Exception:                
                print(".", end="")
        max_window(browser)
        
        # 마우스를 올려놓아야 펼쳐지는 엘리먼트가 있을 경우
        if mouse_xpath:
            try:
                print("마우스 시작")
                a = ActionChains(browser)
                print("a 성공")
                m= browser.find_element_by_xpath(mouse_xpath)
                print("엠=",m)
                a.move_to_element(m).perform()
            except Exception as e:
                print("마우스 오류=", e)
                print("~", end="")
                
        # browser.save_screenshot("courses.png")
        # dom이 모두 준비됨을 기다란다
        # with open('./clipper/jquery-3.6.0.min.js', errors='ignore') as f:
        #     browser.execute_script(f.read())
        # title = browser.execute_script('return $(document).ready(function(){console.log("로딩완료");})')
        print("****", title, "준비됨", "****")
        
        # 타겟엘리먼트가 있으면 엘리먼트의 innerHTML 정보를 수집한다.
        
        blank = False
        try:
            element = browser.find_element_by_xpath(target_xpath)            
        except Exception:
            blank = True
        
        if not blank:            
            html = element.get_attribute("innerHTML")
        
        
        # soup로 만들되 가급적 'lxml' 파서를 이용한다.
            try:
                soup = BeautifulSoup(html, 'lxml')
            except Exception:
                soup = BeautifulSoup(html, 'html.parser')
        else:
            print('Page:Blank')
            soup = None

        if soup:
            print("soup 추출 성공")  
        # browser 세션을 종료하고 브라우저를 닫는다.    
    return soup