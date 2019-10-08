from django.shortcuts import render
from .models import Course, UserCourse, UserCentre
from btbadmin.models import Centre
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from pullingapp import settings
from send_email.views import send_email
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(lambda u: u.groups.filter(name='domain_admins').exists())
def domain_admin_home(request):
    current_user = request.user
    user_centre = UserCentre.objects.get(user_id=current_user.id)

    delete_course = request.POST.get('delete_course')
    if delete_course:
        course = Course.objects.get(id=delete_course)
        course.delete()
        return HttpResponseRedirect('/domain_admin')

    add_new_course = request.POST.get('add_new_course')
    if add_new_course == "new_course":
        course_code = request.POST.get('course_code')
        course_title = request.POST.get('course_title')
        course_start_date = request.POST.get('course_start_date')
        course = Course(code=course_code, title=course_title, start_date=course_start_date, centre_id=user_centre.centre_id, created_date=timezone.now, updated_date=timezone.now)
        course.save()
        return HttpResponseRedirect('/domain_admin')

    courses = Course.objects.filter(centre_id=user_centre.centre_id)
    return render(
        request,
        'domain_admin/domain_admin.html',
        {
            'title': 'Edit course',
            'courses': courses,
        }
    )


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(lambda u: u.groups.filter(name='domain_admins').exists())
def edit_course(request, course_id):
    message = ""
    message_class = ""

    remove_course_user_id = request.POST.get('remove_user')
    if remove_course_user_id:
        course_user = UserCourse.objects.get(course_id=course_id, user_id=remove_course_user_id)
        course_user.delete()

    new_course_user = request.POST.get('add_user_to_course')
    if new_course_user == 'add_new_course_user':
        course_user = request.POST.get('add_course_user')
        # check if user is already on a course
        print(course_user)
        user_on_course = UserCourse.objects.filter(user_id=course_user)
        print(user_on_course.count())
        if user_on_course.count() > 0:
            message = "User is already enrolled on a course"
            message_class = "error-message"
        else:
            user_course = UserCourse(user_id=course_user, course_id=course_id, status=1, created_date=timezone.now, updated_date=timezone.now)
            user_course.save()
            message = str(user_course.user.first_name) + " has been added successfully"
            message_class = "success-message"

    # get centre from user through UserCentre object
    user_centre = Centre.objects.get(course__id=course_id)
    # Get course object from parsed course_id
    course = Course.objects.get(id=course_id)

    # Get course users
    course_users = UserCourse.objects.filter(course_id=course_id)
    course_users_filter = UserCourse.objects.filter(course_id=course_id).values('user_id')

    # Get all centre users
    all_centre_users = UserCentre.objects.filter(centre_id=user_centre)
    all_centre_users_filter = UserCentre.objects.filter(centre_id=user_centre)

    invite_user_email = request.POST.get('invite_user_email')
    invite_user_first_name = request.POST.get('invite_user_first_name')
    current_site = get_current_site(request)
    register_url = current_site.domain + reverse("register")

    ctx = {}
    ctx["first_name"] = invite_user_first_name
    ctx["centre_name"] = user_centre.name
    ctx["course_name"] = course.title
    ctx["register_url"] = current_site.domain + reverse("register")

    emails = (invite_user_email,)
    if invite_user_email:
        send_email(request, "course_invitation", ctx, emails)

    try:
        available_centre_users = all_centre_users.exclude(user_id__in=course_users_filter)
    except ValueError:
        available_centre_users = None

    return render(
        request,
        'domain_admin/edit_course.html',
        {
            'title': 'Edit course',
            'course': course,
            'course_users': course_users,
            'centre': user_centre,
            'available_centre_users': available_centre_users,
            'message': message,
            'message_class': message_class
        }
    )

