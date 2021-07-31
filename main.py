import os
from dotenv import load_dotenv
load_dotenv() # secret_key 불러오기 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()

from clipper.nomad import get_courses as get_nomad_courses
from clipper.course_save import save as course_save

nomad_courses = get_nomad_courses()
course_save(nomad_courses, "nomadcoders")