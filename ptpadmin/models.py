from django.db import models
from btbadmin.models import Centre


class Course(models.Model):
    code = models.CharField("Course code", max_length=50, null=True, blank=True)
    title = models.CharField("Course title", max_length=255, null=False, blank=False)
    centre = models.ForeignKey(Centre, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField("Course start date", null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class UserCourse(models.Model):
    user = models.IntegerField()
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.PositiveIntegerField('Course status', default=0, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

