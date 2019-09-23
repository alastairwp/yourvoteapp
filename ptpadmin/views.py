from django.shortcuts import render
from .models import Course, UserCourse
from django.http import HttpRequest, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from pullingapp import settings


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(lambda u: u.groups.filter(name='ptpadmins').exists())
def ptpadmin_home(request):
    delete_course = request.POST.get('delete_course')
    if delete_course:
        course = Course.objects.get(id=delete_course)
        course.delete()
        return HttpResponseRedirect('/ptpadmin')

    add_new_course = request.POST.get('add_new_course')
    if add_new_course == "new_course":
        course_code = request.POST.get('course_code')
        course_title = request.POST.get('course_title')
        course_start_date = request.POST.get('course_start_date')
        centre = 1
        course = Course(code=course_code, title=course_title, start_date=course_start_date, centre_id=centre, created_date=timezone.now, updated_date=timezone.now)
        course.save()
        return HttpResponseRedirect('/ptpadmin')

    courses = Course.objects.all()
    return render(
        request,
        'ptpadmin/ptpadmin.html',
        {
            'title': 'Centre Admin',
            'courses': courses,
        }
    )


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(lambda u: u.groups.filter(name='ptpadmins').exists())
def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course_users = UserCourse.objects.filter(course_id=course_id)
    return render(
        request,
        'ptpadmin/edit_course.html',
        {
            'title': 'Centre Admin',
            'course': course,
            'course_users': course_users,
        }
    )