from django.shortcuts import render
from ptpadmin.models import UserCourse
from django import template
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(lambda u: u.groups.filter(name='members').exists())
def dashboard(request):
    current_user = request.user
    courses = UserCourse.objects.filter(user=current_user.id)
    return render(
        request,
        'members/dashboard.html',
        {
            'title': 'PtP Dashboard',
            'courses': courses
        }
    )
