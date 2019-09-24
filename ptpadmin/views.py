from django.shortcuts import render
from .models import Course, UserCourse, UserCentre
from django.http import HttpRequest, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from pullingapp import settings


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(lambda u: u.groups.filter(name='ptpadmins').exists())
def ptpadmin_home(request):
    current_user = request.user
    user_centre = UserCentre.objects.get(user_id=current_user.id)

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
        course = Course(code=course_code, title=course_title, start_date=course_start_date, centre_id=user_centre.centre_id, created_date=timezone.now, updated_date=timezone.now)
        course.save()
        return HttpResponseRedirect('/ptpadmin')

    courses = Course.objects.filter(centre_id=user_centre.centre_id)
    return render(
        request,
        'ptpadmin/ptpadmin.html',
        {
            'title': 'Edit course',
            'courses': courses,
        }
    )


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(lambda u: u.groups.filter(name='ptpadmins').exists())
def edit_course(request, course_id):
    new_course_user = request.POST.get('add_user_to_course')
    if new_course_user == 'add_new_course_user':
        course_user = request.POST.get('add_course_user')
        user_course = UserCourse(user_id=course_user, course_id=course_id, status=1, created_date=timezone.now,
                                 updated_date=timezone.now)
        user_course.save()

    # get current_user
    current_user = request.user

    # get centre from user through UserCentre object
    user_centre = UserCentre.objects.get(user_id=current_user.id)

    # Get course object from parsed course_id
    course = Course.objects.get(id=course_id)

    # Get course users
    course_users = UserCourse.objects.filter(course_id=course_id)
    course_users_filter = UserCourse.objects.filter(course_id=course_id).values('user_id')

    # Get all centre users
    all_centre_users = UserCentre.objects.filter(centre_id=user_centre.centre_id)
    all_centre_users_filter = UserCentre.objects.filter(centre_id=user_centre.centre_id)
    available_centre_users = all_centre_users.exclude(user_id__in=course_users_filter)

    return render(
        request,
        'ptpadmin/edit_course.html',
        {
            'title': 'Edit course',
            'course': course,
            'course_users': course_users,
            'centre': user_centre,
            'available_centre_users': available_centre_users
        }
    )

