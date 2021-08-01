"""
크롤링하는데 여러 번 실패해 본 결과, 
다음과 같은 크롤링 전략이 가장 효과적이었다.
1. 셀레늄 웹드라이버로 웹페이지를 얻는다.
2. 셀레늄 execute 명령으로 그 웹페이지의 <html>태그 내용물을 innerHTML로 리턴시켜
3. 만든 soup 객체를 가지고 
4. 분석한다.
https://stackoverflow.com/questions/62165635/how-to-scrape-data-from-flexbox-element-container-with-python-and-beautiful-soup
"""
from requests.compat import urljoin
from bs4 import BeautifulSoup
import re
from clipper.chromer import get_soup_from_page
# constants
BASE_URL = "https://nomadcoders.co/"
COURSES_URL = urljoin(BASE_URL, "/courses")
CHALLENGES_URL = urljoin(BASE_URL, "/challenges")
WAIT = 5 # seconds


def extract_courses(cards):
    
    
    course_info = []

    counter = 1

    for card in cards:
        print(counter, end=" ")
        course = extract_course(card)
        course_info.append(course)
        counter += 1

    return course_info


def extract_course(card):

    # 캐치 못하는 경우 고려
    try:
        title = card.find("h3").get_text(strip=True)
    except Exception:
        title = "-"
    try:
        description = card.find("h4").get_text(strip=True)
    except Exception:
        description = "-"
    try:
        thumbnail_link = card.find("img")["src"]
    except Exception:
        thumbnail_link = "-"

    instructor = "니꼬샘"

    course_link = card.find("a")["href"]
    course_link = urljoin(BASE_URL, course_link)

    chapter_list = extract_chapter_list(course_link)

    return {
        "title" : title,
        "thumbnail_link" : thumbnail_link,
        "description" : description,
        "instructor" : instructor,
        "course_link" : course_link,
        "chapter_list" : chapter_list
    }


# 각 강의의 챕터 목록 추출
def extract_chapter_list(link):
    button_xpath = "//button[contains(text(),'See all')]"
    soup = get_soup_from_page(link, button_xpath=button_xpath)
    curriculum = soup.find('div', string=re.compile("curriculum", re.I))
    chapters = curriculum.parent.find_all('span', string=re.compile("#[0-9][^.][^.]"))
    
    chapter_list = []
    for chapter in chapters:
        chapter_name = chapter.get_text()
        
        section_list = []
        for section in chapter.parent.select("button"):
            section_list.append(section.select_one("span").get_text())
        
        chapter_list.append({
                "chapter" : chapter_name,
                "section_list" : section_list
            })
        
    return chapter_list

def get_courses():
    
    # 이제 soup로 본격적인 스크래이핑 작업에 들어간다.
    soup = get_soup_from_page(COURSES_URL)
    # card가 담긴 태그
    cards = soup.find_all("div", class_="sc-bdfBwQ znekp flex flex-col items-center")
    courses_info = extract_courses(cards)

    return courses_info