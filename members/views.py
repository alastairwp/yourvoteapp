from django.shortcuts import render, render_to_response
from domain_admin.models import UserCourse, Course
from vote.models import Category, SubCategory, Question, Vote
from django import template
from django.contrib.auth.models import Group, User
from domain_admin.models import UserCentre
from btbadmin.models import Centre
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, IntegerField
from django.contrib import messages
from django.http import HttpResponseRedirect


def handler404(request, *args, **argv):
    response = render_to_response("errors/404.html", {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render_to_response("errors/500.html", {})
    response.status_code = 500
    return response


register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@login_required()
def dashboard(request):
    current_user = request.user
    courses = UserCourse.objects.filter(user_id=current_user.id)
    return render(
        request,
        'members/dashboard.html',
        {
            'title': 'Dashboard',
            'courses': courses,
            'active_tab': "dashboard"
        }
    )


@login_required()
def assessmentreport(request, course_id):
    #  check user is registered to this course
    currentuser = User.objects.get(email=request.user)
    if not UserCourse.objects.filter(user_id=currentuser.id, course_id=course_id).exists():
        return HttpResponseRedirect("/404/")

    if lambda u: u.groups.filter(name='domain_admins').exists():
        participant = request.POST.get("participants")
        if participant:
            current_user = participant
        else:
            current_user = currentuser.id
    else:
        current_user = currentuser.id

    course_cohort_avg = Vote.objects.filter(course_id=course_id).aggregate(Avg('value', output_field=IntegerField()))
    if course_cohort_avg['value__avg'] is None:
        course_cohort_avg['value__avg'] = 0
    course_cohort_revised_avg = Vote.objects.filter(course_id=course_id).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if course_cohort_revised_avg['revised_value__avg'] is None:
        course_cohort_revised_avg['revised_value__avg'] = 0

    #  Get average for all users in whole category
    cat1_cohort_avg = Vote.objects.filter(question__subcategory__category=1).filter(course_id=course_id).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat1_cohort_avg['value__avg'] is None:
        cat1_cohort_avg['value__avg'] = 0
    #  Get average for specific user in a category
    cat1avg = Vote.objects.filter(user_id=current_user).filter(course_id=course_id).filter(question__subcategory__category=1).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat1avg['value__avg'] is None:
        cat1avg['value__avg'] = 0
    #  Get revised average for all users in whole category
    cat1_cohort_revised_avg = Vote.objects.filter(question__subcategory__category=1).filter(course_id=course_id).filter(revised_value__gt=0).aggregate(
        Avg('revised_value', output_field=IntegerField()))
    if cat1_cohort_revised_avg['revised_value__avg'] is None:
        cat1_cohort_revised_avg['revised_value__avg'] = 0
    #  Get revised average for specific user in a category
    cat1revisedavg = Vote.objects.filter(user_id=current_user).filter(course_id=course_id).filter(
        question__subcategory__category=1).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat1revisedavg['revised_value__avg'] is None:
        cat1revisedavg['revised_value__avg'] = 0

    cat2_cohort_avg = Vote.objects.filter(question__subcategory__category=2).filter(course_id=course_id).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat2_cohort_avg['value__avg'] is None:
        cat2_cohort_avg['value__avg'] = 0
    cat2avg = Vote.objects.filter(user_id=current_user).filter(question__subcategory__category=2).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat2avg['value__avg'] is None:
        cat2avg['value__avg'] = 0
    cat2_cohort_revised_avg = Vote.objects.filter(question__subcategory__category=2).filter(course_id=course_id).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat2_cohort_revised_avg['revised_value__avg'] is None:
        cat2_cohort_revised_avg['revised_value__avg'] = 0
    cat2revisedavg = Vote.objects.filter(user_id=current_user).filter(question__subcategory__category=2).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat2revisedavg['revised_value__avg'] is None:
        cat2revisedavg['revised_value__avg'] = 0

    cat3_cohort_avg = Vote.objects.filter(question__subcategory__category=3).filter(course_id=course_id).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat3_cohort_avg['value__avg'] is None:
        cat3_cohort_avg['value__avg'] = 0
    cat3avg = Vote.objects.filter(user_id=current_user).filter(question__subcategory__category=3).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat3avg['value__avg'] is None:
        cat3avg['value__avg'] = 0
    cat3_cohort_revised_avg = Vote.objects.filter(question__subcategory__category=3).filter(course_id=course_id).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat3_cohort_revised_avg['revised_value__avg'] is None:
        cat3_cohort_revised_avg['revised_value__avg'] = 0
    cat3revisedavg = Vote.objects.filter(user_id=current_user).filter(question__subcategory__category=3).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat3revisedavg['revised_value__avg'] is None:
        cat3revisedavg['revised_value__avg'] = 0

    cat4_cohort_avg = Vote.objects.filter(question__subcategory__category=4).filter(course_id=course_id).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat4_cohort_avg['value__avg'] is None:
        cat4_cohort_avg['value__avg'] = 0
    cat4avg = Vote.objects.filter(user_id=current_user).filter(question__subcategory__category=4).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat4avg['value__avg'] is None:
        cat4avg['value__avg'] = 0
    cat4_cohort_revised_avg = Vote.objects.filter(question__subcategory__category=4).filter(course_id=course_id).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat4_cohort_revised_avg['revised_value__avg'] is None:
        cat4_cohort_revised_avg['revised_value__avg'] = 0
    cat4revisedavg = Vote.objects.filter(user_id=current_user).filter(question__subcategory__category=4).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat4revisedavg['revised_value__avg'] is None:
        cat4revisedavg['revised_value__avg'] = 0

    cat5_cohort_avg = Vote.objects.filter(question__subcategory__category=5).filter(course_id=course_id).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat5_cohort_avg['value__avg'] is None:
        cat5_cohort_avg['value__avg'] = 0
    cat5avg = Vote.objects.filter(user_id=current_user).filter(question__subcategory__category=5).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat5avg['value__avg'] is None:
        cat5avg['value__avg'] = 0
    cat5_cohort_revised_avg = Vote.objects.filter(question__subcategory__category=5).filter(course_id=course_id).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat5_cohort_revised_avg['revised_value__avg'] is None:
        cat5_cohort_revised_avg['revised_value__avg'] = 0
    cat5revisedavg = Vote.objects.filter(user_id=current_user).filter(question__subcategory__category=5).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat5revisedavg['revised_value__avg'] is None:
        cat5revisedavg['revised_value__avg'] = 0

    cat6_cohort_avg = Vote.objects.filter(question__subcategory__category=6).filter(course_id=course_id).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat6_cohort_avg['value__avg'] is None:
        cat6_cohort_avg['value__avg'] = 0
    cat6avg = Vote.objects.filter(user_id=current_user).filter(question__subcategory__category=6).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat6avg['value__avg'] is None:
        cat6avg['value__avg'] = 0
    cat6_cohort_revised_avg = Vote.objects.filter(question__subcategory__category=6).filter(course_id=course_id).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat6_cohort_revised_avg['revised_value__avg'] is None:
        cat6_cohort_revised_avg['revised_value__avg'] = 0
    cat6revisedavg = Vote.objects.filter(user_id=current_user).filter(question__subcategory__category=6).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat6revisedavg['revised_value__avg'] is None:
        cat6revisedavg['revised_value__avg'] = 0

    cat7_cohort_avg = Vote.objects.filter(question__subcategory__category=7).filter(course_id=course_id).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat7_cohort_avg['value__avg'] is None:
        cat7_cohort_avg['value__avg'] = 0
    cat7avg = Vote.objects.filter(user_id=current_user).filter(question__subcategory__category=7).filter(value__gt=0).aggregate(Avg('value', output_field=IntegerField()))
    if cat7avg['value__avg'] is None:
        cat7avg['value__avg'] = 0
    cat7_cohort_revised_avg = Vote.objects.filter(question__subcategory__category=7).filter(course_id=course_id).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat7_cohort_revised_avg['revised_value__avg'] is None:
        cat7_cohort_revised_avg['revised_value__avg'] = 0
    cat7revisedavg = Vote.objects.filter(user_id=current_user).filter(question__subcategory__category=7).filter(revised_value__gt=0).aggregate(Avg('revised_value', output_field=IntegerField()))
    if cat7revisedavg['revised_value__avg'] is None:
        cat7revisedavg['revised_value__avg'] = 0

    categories = Category.objects.all()
    newcat = True
    newsubcat = True
    reportscores = {}

    for category in categories:
        if newcat is True:
            reportscores = {category.name: 0}  # this sets up the category level in the dictionary
        else:
            reportscores[category.name] = 0

        subcategories = SubCategory.objects.filter(category_id=category.id)
        for subcategory in subcategories:

            if newsubcat is True:
                reportscores[category.name] = {subcategory.name: 0}  # this sets up the subcategory level in the dictionary
            else:
                reportscores[category.name][subcategory.name] = 0

            questions = Question.objects.filter(subcategory_id=subcategory.id)
            totalvotescore = Vote.objects.filter(user_id=current_user).filter(question_id__in=questions).aggregate(Sum('value'))
            totalvoterevisedscore = Vote.objects.filter(user_id=current_user).filter(question_id__in=questions).aggregate(
                Sum('revised_value'))

            try:
                tvs = str(totalvotescore['value__sum'])
                tvs = int(tvs)
            except ValueError:
                tvs = 0

            try:
                tvr = str(totalvoterevisedscore['revised_value__sum'])
                tvr = int(tvr)
            except ValueError:
                tvr = 0

            question_count = len(questions)

            if tvs != 0:
                average_score = tvs / question_count
            else:
                average_score = 0

            if tvr != 0:
                average_revised = tvr / question_count
            else:
                average_revised = 0

            reportscores[category.name][subcategory.name] = {"score": int(average_score), "revised": int(average_revised)}
            newcat = False
            newsubcat = False

        newsubcat = True

    newcat = True

    originalData = [cat1avg['value__avg'], cat2avg['value__avg'], cat3avg['value__avg'], cat4avg['value__avg'],
                    cat5avg['value__avg'], cat6avg['value__avg'], cat7avg['value__avg']]

    revisedData = [cat1revisedavg['revised_value__avg'], cat2revisedavg['revised_value__avg'],
                   cat3revisedavg['revised_value__avg'], cat4revisedavg['revised_value__avg'],
                   cat5revisedavg['revised_value__avg'], cat6revisedavg['revised_value__avg'],
                   cat7revisedavg['revised_value__avg']]

    originalCohortData = [cat1_cohort_avg['value__avg'], cat2_cohort_avg['value__avg'], cat3_cohort_avg['value__avg'], cat4_cohort_avg['value__avg'],
                    cat5_cohort_avg['value__avg'], cat6_cohort_avg['value__avg'], cat7_cohort_avg['value__avg']]

    revisedCohortData = [cat1_cohort_revised_avg['revised_value__avg'], cat2_cohort_revised_avg['revised_value__avg'],
                   cat3_cohort_revised_avg['revised_value__avg'], cat4_cohort_revised_avg['revised_value__avg'],
                   cat5_cohort_revised_avg['revised_value__avg'], cat6_cohort_revised_avg['revised_value__avg'],
                   cat7_cohort_revised_avg['revised_value__avg']]

    participants = UserCourse.objects.filter(course_id=course_id)
    return render(
        request,
        'members/assessment-report.html',
        {
            'title': 'Assessment Report',
            'reportscores': reportscores,
            'cat1avg': cat1avg,
            'cat1revisedavg': cat1revisedavg,
            'cat2avg': cat2avg,
            'cat2revisedavg': cat2revisedavg,
            'cat3avg': cat3avg,
            'cat3revisedavg': cat3revisedavg,
            'cat4avg': cat4avg,
            'cat4revisedavg': cat4revisedavg,
            'cat5avg': cat5avg,
            'cat5revisedavg': cat5revisedavg,
            'cat6avg': cat6avg,
            'cat6revisedavg': cat6revisedavg,
            'cat7avg': cat7avg,
            'cat7revisedavg': cat7revisedavg,
            'gl_cohort_score': cat1_cohort_avg['value__avg'],
            'gl_cohort_revised_score': cat1_cohort_revised_avg['revised_value__avg'],
            'ec_cohort_score': cat2_cohort_avg['value__avg'],
            'ec_cohort_revised_score': cat2_cohort_revised_avg['revised_value__avg'],
            'ci_cohort_score': cat3_cohort_avg['value__avg'],
            'ci_cohort_revised_score': cat3_cohort_revised_avg['revised_value__avg'],
            'bp_cohort_score': cat4_cohort_avg['value__avg'],
            'bp_cohort_revised_score': cat4_cohort_revised_avg['revised_value__avg'],
            'rp_cohort_score': cat5_cohort_avg['value__avg'],
            'rp_cohort_revised_score': cat5_cohort_revised_avg['revised_value__avg'],
            'esu_cohort_score': cat6_cohort_avg['value__avg'],
            'esu_cohort_revised_score': cat6_cohort_revised_avg['revised_value__avg'],
            'ao_cohort_score': cat7_cohort_avg['value__avg'],
            'ao_cohort_revised_score': cat7_cohort_revised_avg['revised_value__avg'],
            'course_cohort_avg': course_cohort_avg['value__avg'],
            'course_cohort_revised_avg': course_cohort_revised_avg['revised_value__avg'],
            'originalData': originalData,
            'revisedData': revisedData,
            'originalCohortData': originalCohortData,
            'revisedCohortData': revisedCohortData,
            'participants': participants,
            'course_id': course_id,
            'current_user': int(current_user)
        }
    )


@login_required()
def course_home(request, course_code):
    #  get current user object
    current_user = User.objects.get(email=request.user)
    # get course object from code in the URL
    course_from_url = Course.objects.get(code=course_code)
    user_course = UserCourse.objects.get(user_id=current_user.id)
    course_from_user = Course.objects.get(id=user_course.course_id)

    #  check is user belongs to the course
    if str(course_from_user.code) != str(course_from_url.code):
        return HttpResponseRedirect('/404/')

    return render(
        request,
        'members/course_home_page.html',
        {
            'title': 'Course Home',
            'course': course_from_url
        }
    )


@login_required()
def account_profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    if str(profile_user.email) == str(request.user):
        if request.method == 'POST':
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1:
                if password1 == password2:
                    profile_user.set_password(password1)
                    profile_user.save()
                    User.objects.filter(pk=user_id).update(first_name=first_name, last_name=last_name)
                    profile_user = User.objects.get(pk=user_id)
                    messages.success(request, 'Password reset successfully')

                else:
                    messages.warning(request, 'Passwords do not match')

            else:
                User.objects.filter(pk=user_id).update(first_name=first_name, last_name=last_name)
                profile_user = User.objects.get(pk=user_id)
                messages.success(request, 'Profile updated successfully')

        user_centre = UserCentre.objects.get(user_id=user_id)
        centre = Centre.objects.get(id=user_centre.centre_id)
    else:
        return HttpResponseRedirect('/404/')

    return render(
        request,
        'members/account-profile.html',
        {
            'title': 'Course Home',
            'user_id': user_id,
            'profile_user': profile_user,
            'centre': centre,
        }
    )



