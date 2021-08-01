import requests
from requests.compat import urljoin, quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import pprint
from clipper.chromer import get_soup_from_page
### constants ###

BASE_URL = "https://coloso.co.kr/"
WAIT = 10 # seconds


def extract_courses(cat_url):
    """
    coloso 사이트에는 두 가지 경우의 강의목록 표시방법이 사용된다. 그래서
    target_xpath도 두 가지를 준비한다.
    """
    # "모든 클래스"라는 text가 들어있는 아무 엘리먼트를 자손엘리먼트로 가지는 section 엘리먼트
    # //section[.//*[contains(text(), "모든 클래스")]]
    # 의 형제들 중 두 번째 section 엘리먼트
    # /following-sibling::section[2]
    target_xpath = '//section[.//*[contains(text(), "모든 클래스")]]/following-sibling::section[2]' \
         '| //*[contains(@class, "catalog-title")]/following-sibling::ul'
    soup = get_soup_from_page(cat_url, target_xpath=target_xpath)
    
    courses_info = []
    for card in soup.find_all('li', class_=re.compile("[^info]")):
        course = extract_course(card)        
        print(".", end="")
        courses_info.append(course)
    
    return courses_info

def extract_course(card):
    try:
        title = card.find(class_=re.compile("title")).get_text(strip=True)
        print(title)
    except Exception:
        title = "-"
    try:
        thumbnail_link = card.find("img")["src"]
    except Exception:
        thumbnail_link = "-"
    try:
        instructor = card.find_all(string=re.compile("."))[-1]
    except Exception:
        instructor = "-"
        
    course_link = card.find('a')["href"]
    course_link = urljoin(BASE_URL, course_link)
    print(course_link)
    description, chapter_list = extract_details(course_link)    

    return {'title': title,
            'thumbnail_link': thumbnail_link,
            'description': description,
            'instructor': str(instructor).strip(),
            'course_link': course_link,
            'chapter_list': chapter_list
            }

def extract_details(link):
    soup = get_soup_from_page(link)
    try:
        description = soup.find('div', class_="fc-card__text").get_text(strip=True)
    except Exception:
        description = "-"
    
    chapter_list = []
    for chapter in soup.select('ol'):
        try:
            chapter_title = chapter.parent.p.get_text(strip=True)
        except Exception:
            chapter_title = "-"
        
        section_list = []
        for section in chapter.find_all('li'):
            try:
                section_title = section.get_text(strip=True)
            except Exception:
                section_title = "-"
            section_list.append(section_title)
        
        chapter_list.append({
            'chapter': chapter_title,
            'section_list': section_list                 
            })
            
    if not chapter_list:
        try:
            parts = soup.find_all(string=re.compile("^PART"))
            sections = soup.find_all('ul', class_='container__cards')
        except Exception as e:
            print(e)
            
        for part, section in zip(parts, sections):
            section_list = section.find_all(string=re.compile("^SECTION"))
            chapter_list.append({
                'chapter': str(part).strip(),
                'section_list': section_list
                })
    
    return description, chapter_list

# 먼저 카테고리를 추출한다.
def get_categories(soup):
    href_list = []
    for ele in soup:
        href_list.append(urljoin(BASE_URL, ele['href']))
    return href_list

def get_courses():
    # 옵션설정 및 리턴값 초기화
    courses_info = []

    # 마우스 오버로 활성화되는 카테고리 리스트 xpath
    # //*[@id="__layout"]/header/div/nav/div/div[3]/ul/li[3]/a
    mouse_xpath = '//*[@id="nav-menu-2"]'
    target_xpath = '//*[@id="nav-menu-2"]/..'
    soup = get_soup_from_page(BASE_URL, target_xpath=target_xpath, mouse_xpath=mouse_xpath)
    category_links = soup.find('ul').find_all('a')
    category_links = get_categories(category_links)
    print(category_links)


    for category in category_links: 
        print("")
        print(category)
        courses = extract_courses(category)
        courses_info += courses
    return courses_info