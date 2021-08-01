import requests
from requests.compat import urljoin, quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
from clipper.chromer import get_soup_from_page
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

### constants ###

BASE_URL = "https://www.udemy.com"

##대상 카테고리
# a. 개발
# b. IT 및 소프트웨어
# c. 디자인
# d. 음악 - 음악 소프트웨어
CATEGORIES = {
    "개발": "/ko/courses/development",
    "IT 및 소프트웨어": "/ko/courses/it-and-software",
    "디자인": "/ko/courses/design",
    "음악 소프트웨어": "/ko/courses/music/music-software"    
}

## 검색조건식 적용 순서
# 1. 한국어 + 가장 인기 있는
# 2. 영어 + 가장 인기 있는 + 평가>4.5
KEYS = [
    ("?lang=ko", "&sort=popularity"),
    ("?lang=en", "&rating=4.5&sort=popularity")
    ]

WAIT = 10 # seconds
TIMES = 5 # 시도 횟수

def url_exists(url):
    response = ''
    try:
        URLValidator(url)
        response = requests.get(url)
    except Exception as e:
        print(e)
    return response

def extract_course(card):

    # 캐치 못하는 경우 고려
    try:
        title = card.find("div", class_=re.compile("title")).get_text(strip=True)
    except Exception:
        title = "-"
    try:
        description = card.find('p', class_=re.compile("course-headline")).get_text(strip=True)
    except Exception:
        description = "-"
    try:
        thumbnail_link = card.find("img")["src"]
    except Exception:
        thumbnail_link = "-"
    try:
        instructor = card.find('div', class_=re.compile("instructor")).get_text(strip=True)
    except Exception:
        instructor = "-"

    course_link = card["href"]
    course_link = urljoin(BASE_URL, course_link)

    # url check
    assert url_exists(course_link)

    chapter_list = extract_chapter_list(course_link)

    return {
        "title" : title,
        "thumbnail_link" : thumbnail_link,
        "description" : description,
        "instructor" : instructor,
        "course_link" : course_link,
        "chapter_list" : chapter_list
    }


def extract_courses(cards):
    """
    한 페이지에서 추출할 수 있는 강의들 정보를 리스트형태로 반환한다,
    """
    courses_info = []

    for card in cards:
        courses_info.append(extract_course(card))
        print(",", end="")
        
    return  courses_info

def extract_chapter_list(link):
    # 옵션설정 및 리턴값 초기화
    chapter_list = []
    
    target_xpath = '//div[@data-purpose="course-curriculum"]'
    # 모든 섹션 확장 button_xpath
    button_xpath = '//button[@data-purpose="expand-toggle"]'
    # 최대 TIMES회 시도
    for i in range(TIMES):
        try:
            soup = get_soup_from_page(link, target_xpath=target_xpath, button_xpath=button_xpath)
        except Exception:
            print("아무내용없이 저장됨")
            soup = None
        if soup:
            break
    chapters = soup.find_all("div", class_=re.compile("section--panel"))
    for chapter in chapters:
        section_list = []
        for section in chapter.find_all("li"):
            section_list.append(section.get_text(strip=True))
        title = chapter.find("span", class_=re.compile("title")).get_text(strip=True)
        chapter_list.append({
                    "chapter": title,
                    "section_list": section_list
                    })
        
    return chapter_list


def get_courses():
    
    courses_info = [] 
    
    # 스크래이핑 시작 페이지 url 결정하기      
    for _, cat in CATEGORIES.items():
        category_url = urljoin(BASE_URL, cat)
        # url check
        assert url_exists(category_url)

        for key in KEYS: 
            # 페이지 번호, 최대 페이지번호, 강의 갯수를 초기화한다.
            page = 0
            max_page = 1
            number_of_courses = 0
            # 페이지 번호가 10 이하에 올려진 강의들만 추출한다.
            # max_page 최소값을 조정해야 한다.
            while page >= 0 and page <= min(max_page, 10):                
                if page:
                    url = urljoin(category_url, key[0] + f"&p={page}" + key[1])
                else:
                    url = urljoin(category_url, "".join(key))
                    print("")
                    print(f"==={url}===")

                
                # 이제 soup로 본격적인 스크래이핑 작업에 들어간다.
                # 원하는 정보가 모두 담긴 최소외각의 xpath는 다음과 같다.
                target_xpath = '//div[contains(@class,"course-directory--container")]'            
                # TIMES회 시도
                for i in range(TIMES):
                    try:
                        soup = get_soup_from_page(url, target_xpath=target_xpath)
                    except Exception:
                        print("아무내용없이 저장됨")
                        soup = None
                    if soup:
                        break
                # 먼저 강의 수에 따라 페이지가 나뉠 수 있으므로 처음 한 번만 체크하고 기록한다.
                if page == 0:
                    page += 1   
                    try:
                        number_of_courses = soup.find('span', string=re.compile("개의 결과"))
                        number_of_courses = int(re.findall("\d+", number_of_courses.get_text())[0])
                    except Exception:
                        number_of_courses = 0


                print(page, end="page: ")

                if number_of_courses > 16:
                    max_page =  number_of_courses // 16 + 1
                # 강의수가 16 개 초과이면 max_page >= 2 이므로 루프를 돈다.     
                page += 1
                cards = soup.select('a[id]')
                courses_info += extract_courses(cards)    

    return courses_info 

