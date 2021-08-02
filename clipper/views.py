from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# from clipper.nomad import get_courses as get_nomad_courses
# from clipper.course_save import save as course_save



def index(request):
    return HttpResponse("성공!")
# def nomad(request):
#     print("노마드")
#     nomad_courses = get_nomad_courses()
#     course_save(nomad_courses, "nomadcoders")
#     return HttpResponse("nomad 강의들을 저장합니다.")