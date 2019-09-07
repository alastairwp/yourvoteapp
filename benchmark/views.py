from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User,auth
from .models import Question, Vote, Hint, UserCourse
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
from django.utils import timezone
from django.core import serializers
from django.views.decorators.csrf import requires_csrf_token

import json


def save_vote_data(request):
    if request.is_ajax():

        current_user = request.user
        question_id = request.POST['question_id']
        value_data = request.POST['value']
        comment_data = request.POST['question_comment']
        course_id = request.POST['course_id']
        now = timezone.now()

        try:
            checkvote = Vote.objects.filter(user__exact=current_user.id, question_id__exact=question_id, course_id=course_id).count()
        except Question.DoesNotExist:
            checkvote = 0

        if checkvote != 0:
            checkvote = Vote.objects.get(user__exact=current_user.id, question_id__exact=question_id, course_id=course_id)
            checkvote.save()
            Vote.objects.filter(id=checkvote.id).update(comment_data=comment_data, value=value_data, course_id=course_id, updated_date=now)
        else:
            savequestion = Vote(user=current_user.id, question_id=question_id, value=value_data, comment_data=comment_data, course_id=course_id, updated_date=now)
            savequestion.save()

        return JsonResponse({'resultdata': 1})
        # var question = Question('')


def save_comment_data(request):
    if request.is_ajax():

        current_user = request.user
        question_id = request.POST['question_id']
        comment_data = request.POST['question_comment']
        course_id = request.POST['course_id']
        now = timezone.now()

        try:
            checkvote = Vote.objects.filter(user__exact=current_user.id, question_id__exact=question_id, course_id=course_id).count()
        except Question.DoesNotExist:
            checkvote = 0

        if checkvote != 0:
            checkvote = Vote.objects.get(user__exact=current_user.id, question_id__exact=question_id, course_id=course_id)
            checkvote.save()
            Vote.objects.filter(id=checkvote.id).update(comment_data=comment_data, updated_date=now)
        else:
            savequestion = Vote(user=current_user.id, question_id=question_id, comment_data=comment_data, updated_date=now)
            savequestion.save()

        return JsonResponse({'resultdata': 1})
        # var question = Question('')


def get_chart_data(request):
    question_id = request.POST['question_id']
    course_id = request.POST['course_id']
    # print(course_id)

    allVote = Vote.objects.filter(question_id__exact=question_id, course_id=course_id)

    tmpJson = serializers.serialize("json", allVote)
    tmpObj = json.loads(tmpJson)

    return JsonResponse({'alldata': tmpObj})


def homepage(request):
    return render(
        request,
        'index.html',
        {
            'title': 'PtP homepage',
        }
    )


def benchmark(request):
    try:
        getid = request.GET['id_data']
    except MultiValueDictKeyError:
        getid = False

    current_user = request.user
    if current_user.is_authenticated:

        if getid==False:
            try:
                question = Question.objects.order_by('id').first()

            except Question.DoesNotExist:
                question = None

            if question!=None:
                question_id = question.id
            else:
                question_id = ''

        else:
            question_id = getid

        if question_id != '':
            try:
                questiondata = Question.objects.get(id__exact=question_id)
            except Question.DoesNotExist:
                questiondata = None

            try:
                next_issue = Question.objects.filter(id__gt=question_id).order_by('id').first()
            except Question.DoesNotExist:
                next_issue = None

            try:
                last_issue = Question.objects.filter(id__lt=question_id).order_by('-id').first()
            except Question.DoesNotExist:
                last_issue = None

            try:
                left_hints = Hint.objects.filter(question_id__exact=question_id).filter(position__exact='l')
            except Hint.DoesNotExist:
                left_hints = None

            try:
                middle_hints = Hint.objects.filter(question_id__exact=question_id).filter(position__exact='m')
            except Hint.DoesNotExist:
                middle_hints = None

            try:
                right_hints = Hint.objects.filter(question_id__exact=question_id).filter(position__exact='r')
            except Hint.DoesNotExist:
                right_hints = None

            try:
                vote_data = Vote.objects.get(question_id__exact=question_id, user__exact=current_user.id)
            except Vote.DoesNotExist:
                vote_data = None

            try:
                usercourse = UserCourse.objects.get(user__exact=current_user.id)
            except UserCourse.DoesNotExist:
                usercourse = None

        else:
            questiondata = None
            next_issue = None
            vote_data = None

        return render(
            request,
            'members/benchmark.html',
            {
                'question': questiondata,
                'question_id': question_id,
                'next_id': next_issue,
                'back_id': last_issue,
                'left_hints':  left_hints,
                'middle_hints': middle_hints,
                'right_hints': right_hints,
                'vote_data': vote_data,
                'course_id': usercourse.course_id
            }
        )

    else:
        return redirect('/login')










