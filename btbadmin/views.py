from django.shortcuts import render
from .models import Centre
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from pullingapp import settings
from django.urls import reverse



@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(lambda u: u.groups.filter(name='btbadmins').exists())
def btbadmin_home(request):
    delete_centre = request.POST.get('delete_centre')
    if delete_centre:
        centre = Centre.objects.get(id=delete_centre)
        centre.delete()
        return HttpResponseRedirect('/btbadmin')

    add_new_centre = request.POST.get('add_new_centre')
    if add_new_centre == "new_centre":
        centre_name = request.POST.get('centre_name')
        centre = Centre(name=centre_name)
        centre.save()
        return HttpResponseRedirect('/btbadmin')

    delete_group = request.POST.get('delete_group')
    if delete_group:
        group = Group.objects.get(id=delete_group)
        group.delete()
        return HttpResponseRedirect('/btbadmin')

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
        return HttpResponseRedirect('/btbadmin/centre/' + centre_id)

    return render(
        request,
        'btbadmin/edit_centre.html',
        {
            'centre': centre,
            'admin_groups': admin_groups
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