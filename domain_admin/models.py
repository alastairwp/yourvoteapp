from django.db import models
from btbadmin.models import Centre
from django.contrib.auth.models import User


class Course(models.Model):
    code = models.CharField("Course code", max_length=50, null=True, blank=True)
    title = models.CharField("Course title", max_length=255, null=False, blank=False)
    centre = models.ForeignKey(Centre, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField("Course start date", null=True, blank=True)
    status = models.PositiveIntegerField("Stage", null=True, blank=True, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class UserCourse(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.PositiveIntegerField('Course status', default=0, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class UserCentre(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    centre = models.ForeignKey(Centre, null=False, blank=False, on_delete=models.CASCADE)
