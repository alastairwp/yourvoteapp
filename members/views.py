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

#  ----------------------
#  Assessment QuerySets -
#  ----------------------
    course_cohort_avg = Vote.objects.filter(course_id=course_id).aggregate(Avg('value'))
    if course_cohort_avg['value__avg'] is None:
        course_cohort_avg['value__avg'] = 0
    course_cohort_revised_avg = Vote.objects.filter(course_id=course_id).filter(revised_value__gt=0).aggregate(Avg('revised_value'))
    if course_cohort_revised_avg['revised_value__avg'] is None:
        course_cohort_revised_avg['revised_value__avg'] = 0

    # get all the cohort averages by category
    cohort_averages_by_category = Vote.objects.values('question__subcategory__category__name').annotate(Avg('value'), Avg('revised_value')).filter(course_id=3).filter(value__gt=0).order_by('question__subcategory__category__id')

    # get all the cohort averages by sub-category
    user_averages_by_category = Vote.objects.values('question__subcategory__category__name').annotate(Avg('value'), Avg('revised_value')).filter(course_id=3).filter(value__gt=0).filter(user_id=current_user).order_by('question__subcategory__category__id')

    # get all the cohort averages by sub-category
    user_averages_by_subcategory = Vote.objects.values('question__subcategory__category__name', 'question__subcategory__name').annotate(Avg('value'), Avg('revised_value')).filter(course_id=3).filter(value__gt=0).filter(user_id=current_user).order_by('question__subcategory__id')

    full_question_set = Question.objects.all().order_by('number')
    #  get number of questions answered
    course = Course.objects.get(id=course_id)
    question_answer_set = {}

    questions_answered = Vote.objects.filter(user_id=current_user, course_id=course_id).exclude(value=0)
    questions_answered_ids = Vote.objects.filter(user_id=current_user, course_id=course_id).order_by('question_id').values_list('question_id')
    questions_answered_count = questions_answered.count()
    for question in full_question_set:
        blnSwitch = False
        for answered_question in questions_answered_ids:
            if question.id in answered_question:
                vote = Vote.objects.filter(user_id=current_user, course_id=course_id, question_id=question.id).order_by('-created_date')[:1].get()
                if vote:
                    question_answer_set[question.id] = (question.name, vote.value, vote.revised_value)
                else:
                    question_answer_set[question.id] = (question.name, 0, 0)
                blnSwitch = True
                break

        if blnSwitch is False:
            try:
                vote = Vote.objects.filter(user_id=current_user, course_id=course_id, question_id=question.id).order_by('-created_date')[:1].get()
                question_answer_set[question.id] = (question.name, vote.value, vote.revised_value)
            except Vote.DoesNotExist:
                question_answer_set[question.id] = (question.name, 0)

#  -----------------------
#  Radar chart QuerySets -
#  -----------------------
    radar_user_category_averages = []
    for user_category_average in user_averages_by_category:
        radar_user_category_averages.append(user_category_average['value__avg'])

    radar_user_category_revised_averages = []
    for user_category_revised_average in user_averages_by_category:
        radar_user_category_revised_averages.append(user_category_revised_average['revised_value__avg'])

    radar_cohort_category_averages = []
    for cohort_category_average in cohort_averages_by_category:
        radar_cohort_category_averages.append(cohort_category_average['value__avg'])

    radar_cohort_category_revised_averages = []
    for cohort_category_revised_average in cohort_averages_by_category:
        radar_cohort_category_revised_averages.append(cohort_category_revised_average['revised_value__avg'])

    participants = UserCourse.objects.filter(course_id=course_id)
    return render(
        request,
        'members/assessment-report.html',
        {
            'title': 'Assessment Report',
            'course_cohort_avg': course_cohort_avg['value__avg'],
            'course_cohort_revised_avg': course_cohort_revised_avg['revised_value__avg'],
            'radar_user_category_averages': radar_user_category_averages,
            'radar_user_category_revised_averages': radar_user_category_revised_averages,
            'radar_cohort_category_averages': radar_cohort_category_averages,
            'radar_cohort_category_revised_averages': radar_cohort_category_revised_averages,
            'participants': participants,
            'course_id': course_id,
            'current_user': int(current_user),
            'full_question_set': full_question_set,
            'questions_answered_count': questions_answered_count,
            'question_answer_set': question_answer_set,
            'cohort_averages_by_category': cohort_averages_by_category,
            'user_averages_by_subcategory': user_averages_by_subcategory,
            'user_averages_by_category': user_averages_by_category,
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



