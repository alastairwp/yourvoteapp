from django.shortcuts import render
from domain_admin.models import UserCourse
from vote.models import Category, SubCategory, Question, Vote
from django import template
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, IntegerField
from django.contrib.auth.views import PasswordResetView

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
            'title': 'PtP Dashboard',
            'courses': courses
        }
    )


@login_required()
def assessmentreport(request):
    current_user = request.user

    cat1avg = Vote.objects.filter(user_id=current_user.id).filter(question__subcategory__category=1).aggregate(Avg('value', output_field=IntegerField()))
    if cat1avg['value__avg'] is None:
        cat1avg['value__avg'] = 0

    cat2avg = Vote.objects.filter(user_id=current_user.id).filter(question__subcategory__category=2).aggregate(Avg('value', output_field=IntegerField()))
    if cat2avg['value__avg'] is None:
        cat2avg['value__avg'] = 0

    cat3avg = Vote.objects.filter(user_id=current_user.id).filter(question__subcategory__category=3).aggregate(Avg('value', output_field=IntegerField()))
    if cat3avg['value__avg'] is None:
        cat3avg['value__avg'] = 0

    cat4avg = Vote.objects.filter(user_id=current_user.id).filter(question__subcategory__category=4).aggregate(Avg('value', output_field=IntegerField()))
    if cat4avg['value__avg'] is None:
        cat4avg['value__avg'] = 0

    cat5avg = Vote.objects.filter(user_id=current_user.id).filter(question__subcategory__category=5).aggregate(Avg('value', output_field=IntegerField()))
    if cat5avg['value__avg'] is None:
        cat5avg['value__avg'] = 0

    cat6avg = Vote.objects.filter(user_id=current_user.id).filter(question__subcategory__category=6).aggregate(Avg('value', output_field=IntegerField()))
    if cat6avg['value__avg'] is None:
        cat6avg['value__avg'] = 0

    cat7avg = Vote.objects.filter(user_id=current_user.id).filter(question__subcategory__category=7).aggregate(Avg('value', output_field=IntegerField()))
    if cat7avg['value__avg'] is None:
        cat7avg['value__avg'] = 0

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
            totalvotescore = Vote.objects.filter(user_id=current_user.id).filter(question_id__in=questions).aggregate(Sum('value'))

            try:
                tvs = str(totalvotescore['value__sum'])
                tvs = int(tvs)
            except ValueError:
                tvs = 0

            question_count = len(questions)
            if tvs != 0:
                average_score = tvs / question_count
            else:
                average_score = 0
            reportscores[category.name][subcategory.name] = {"score": int(average_score), "revised": int(0)}
            newcat = False
            newsubcat = False

        newsubcat = True
    newcat = True

    return render(
        request,
        'members/assessment-report.html',
        {
            'title': 'Assessment Report',
            'reportscores': reportscores,
            'cat1avg': cat1avg,
            'cat2avg': cat2avg,
            'cat3avg': cat3avg,
            'cat4avg': cat4avg,
            'cat5avg': cat5avg,
            'cat6avg': cat6avg,
            'cat7avg': cat7avg,
        }
    )