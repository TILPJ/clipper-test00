from clipper.models import Site, Course, Chapter, Section

# 섹션 정보 저장
def section_info_save(chapter, section_list):

    for section in section_list:
        data = Section(id=None,
                       name=section[:500],
                       chapter=chapter
                    )
        data.save()


# 챕터 정보 저장
def chapter_info_save(course, chapter_list):
    
    for chapter in chapter_list:        
        data = Chapter(id=None,
                       name=chapter["chapter"][:500],
                       course=course
                    )
        data.save()
        
        section_list = chapter["section_list"]
        section_info_save(data, section_list)


# 강의 정보 저장 
def course_info_save(courses, site_):
    
    for course in courses:
        # data unpacking
        # 기존에 해당 코스가 DB에 저장되어 있는지 파악을 시도하고
        # 저장되지 않았다면 get함수는 오류를 발생시키므로 (filter는 empty query)
        # 오류를 캐취하면 DB에 저장하도록 한다.
        try:
            crs = Course.objects.get(course_link=course["course_link"])
        except Exception:
            data = Course(id=None,
                          title=course["title"][:500], 
                          thumbnail_link=course["thumbnail_link"], 
                          description=course["description"], 
                          instructor=course["instructor"][:300], 
                          course_link=course["course_link"], 
                          site=site_
                        )
            data.save()
        
            chapter_list = course["chapter_list"]
            chapter_info_save(data, chapter_list)

    
# inflean.py 파일에서 스크랩하여 저장한 리스트를 받아서 데이터베이스에 저장
def save(courses, site_name):

    try:
        site = Site.objects.get(name__contains=site_name)
    except Exception:
        site = Site(name=site_name)
        site.save()

    course_info_save(courses, site)