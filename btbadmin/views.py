from django.shortcuts import render
from .models import Centre
from domain_admin.models import Course, UserCourse, UserCentre
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from pullingapp import settings
from django.urls import reverse
from django.utils import timezone


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(lambda u: u.groups.filter(name='btbadmins').exists())
def btbadmin_home(request):
    delete_centre = request.POST.get('delete_centre')
    if delete_centre:
        centre = Centre.objects.get(id=delete_centre)
        centre.delete()
        return HttpResponseRedirect(reverse('btbadmin_home'))

    add_new_centre = request.POST.get('add_new_centre')
    if add_new_centre == "new_centre":
        centre_name = request.POST.get('centre_name')
        centre = Centre(name=centre_name)
        centre.save()
        return HttpResponseRedirect(reverse('btbadmin_home'))

    delete_group = request.POST.get('delete_group')
    if delete_group:
        group = Group.objects.get(id=delete_group)
        group.delete()
        return HttpResponseRedirect(reverse('btbadmin_home'))

    add_new_group = request.POST.get('add_new_group')
    if add_new_group == "new_group":
        group_name = request.POST.get('group_name')
        group = Group(name=group_name)
        group.save()
        return HttpResponseRedirect(reverse('btbadmin_home'))

    all_users = User.objects.all()
    all_groups = Group.objects.all()
    centres = Centre.objects.all()

    return render(
        request,
        'btbadmin/btbadmin.html',
        {
            'title': 'BtB Admin',
            'centres': centres,
            'all_users': all_users,
            'all_groups': all_groups,
        }
    )


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(lambda u: u.groups.filter(name='btbadmins').exists())
def edit_centre(request, centre_id):
    centre = Centre.objects.get(id=centre_id)
    admin_groups = Group.objects.all()

    update_centre = request.POST.get('update_centre')
    if update_centre:
        centre_name = request.POST.get('centre_name')
        admin_group_id = request.POST.get('admin_group')
        centre = Centre.objects.get(id=update_centre)
        centre.name = centre_name
        if admin_group_id != 0:
            centre.admin_user_group_id = admin_group_id
        else:
            centre.admin_user_group_id = 0
        centre.save()
        return HttpResponseRedirect(reverse('edit_centre') + centre_id)

    delete_course = request.POST.get('delete_course')
    if delete_course:
        course = Course.objects.get(id=delete_course)
        course.delete()
        return HttpResponseRedirect(reverse('edit_centre') + centre_id)

    add_new_course = request.POST.get('add_new_course')
    if add_new_course == "new_course":
        course_code = request.POST.get('course_code')
        course_title = request.POST.get('course_title')
        course_start_date = request.POST.get('course_start_date')
        course = Course(code=course_code, title=course_title, start_date=course_start_date,
                        centre_id=centre_id, created_date=timezone.now, updated_date=timezone.now)
        course.save()
        return HttpResponseRedirect(reverse('edit_centre') + centre_id)

    courses = Course.objects.filter(centre_id=centre_id)

    return render(
        request,
        'btbadmin/edit_centre.html',
        {
            'centre': centre,
            'admin_groups': admin_groups,
            'courses': courses
        }
    )


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(lambda u: u.groups.filter(name='btbadmins').exists())
def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    save_groups = request.POST.get('save_groups')
    if save_groups:
        selected_groups = request.POST.getlist('groups[]')
        all_groups = Group.objects.all()
        for group in all_groups:
            if str(group.id) in selected_groups:
                g = Group.objects.get(id=group.id)
                g.user_set.add(user)
            else:
                g = Group.objects.get(id=group.id)
                g.user_set.remove(user)

    my_groups = user.groups.all()
    all_groups = Group.objects.all()

    return render(
        request,
        'btbadmin/edit_user.html',
        {
            'user': user,
            'all_groups': all_groups,
            'my_groups': my_groups,
        }
    )


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(lambda u: u.groups.filter(name='btbadmins').exists())
def edit_course(request, course_id):
    remove_course_user_id = request.POST.get('remove_user')
    if remove_course_user_id:
        course_user = UserCourse.objects.get(course_id=course_id, user_id=remove_course_user_id)
        course_user.delete()

    new_course_user = request.POST.get('add_user_to_course')
    if new_course_user == 'add_new_course_user':
        course_user = request.POST.get('add_course_user')
        user_course = UserCourse(user_id=course_user, course_id=course_id, status=1, created_date=timezone.now,
                                 updated_date=timezone.now)
        user_course.save()

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

    try:
        available_centre_users = all_centre_users.exclude(user_id__in=course_users_filter)
    except ValueError:
        available_centre_users = None

    return render(
        request,
        'btbadmin/edit_course.html',
        {
            'title': 'Edit course',
            'course': course,
            'course_users': course_users,
            'centre': user_centre,
            'available_centre_users': available_centre_users
        }
    )


