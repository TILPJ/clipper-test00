from django.db import models

# 추가 
class Site(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=500)
    thumbnail_link = models.URLField(max_length=500, null=True)
    description = models.TextField(null=True)
    instructor = models.CharField(max_length=300, null=True)
    course_link = models.URLField(max_length=500)
    site = models.ForeignKey(Site, on_delete=models.CASCADE) # add 

    def __str__(self):
        return self.title


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)    
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    

class Section(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

