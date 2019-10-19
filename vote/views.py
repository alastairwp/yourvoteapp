from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from .models import Question, Vote, Hint
from domain_admin.models import UserCourse, Course
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
from django.utils import timezone
from django.core import serializers
from django.conf import settings
from django.views.decorators.csrf import requires_csrf_token
import json
from django.urls import reverse


def save_vote_data(request):
    if request.is_ajax():
        current_user = request.user
        question_id = request.POST['question_id']
        value_data = request.POST['value']
        comment_data = request.POST['question_comment']
        course_id = request.POST['course_id']
        now = timezone.now()

        #  Is the course at 1st or 2nd stage? If 2nd Stage then the vote-value is the revised-value
        course = Course.objects.get(id=course_id)

        try:
            checkvote = Vote.objects.filter(user__exact=current_user.id, question_id__exact=question_id,
                                            course_id=course_id).count()
        except Question.DoesNotExist:
            checkvote = 0

        if checkvote != 0:
            checkvote = Vote.objects.get(user__exact=current_user.id, question_id__exact=question_id,
                                         course_id=course_id)
            checkvote.save()
            if course.status == 0:
                Vote.objects.filter(id=checkvote.id).update(comment_data=comment_data, value=value_data,
                                                            course_id=course_id, updated_date=now)
            elif course.status == 1:
                Vote.objects.filter(id=checkvote.id).update(comment_data=comment_data, revised_value=value_data,
                                                            course_id=course_id, updated_date=now)

        else:
            savequestion = Vote(user=current_user, question_id=question_id, value=value_data,
                                comment_data=comment_data, course_id=course_id, updated_date=now)
            savequestion.save()

        return JsonResponse({'resultdata': 1})


def save_comment_data(request):
    if request.is_ajax():
        current_user = request.user
        question_id = request.POST['question_id']
        comment_data = request.POST['question_comment']
        try:
            course_id = request.POST['course_id']
        except MultiValueDictKeyError:
            course_id = None
        now = timezone.now()
        try:
            checkvote = Vote.objects.filter(user_id=current_user.id, question_id__exact=question_id, course_id=course_id).count()
        except Question.DoesNotExist:
            checkvote = 0

        if checkvote != 0:
            checkvote = Vote.objects.get(user_id=current_user.id, question_id__exact=question_id, course_id=course_id)
            checkvote.save()
            Vote.objects.filter(id=checkvote.id).update(comment_data=comment_data, updated_date=now)
        else:
            savequestion = Vote(user_id=current_user.id, question_id=question_id, comment_data=comment_data, updated_date=now)
            savequestion.save()

        return JsonResponse({'resultdata': 1})
        # var question = Question('')


def get_chart_data(request):
    try:
        question_id = request.POST['question_id']
    except MultiValueDictKeyError:
        question_id = None

    try:
        course_id = request.POST['course_id']
    except MultiValueDictKeyError:
        course_id = None

    allVote = Vote.objects.filter(question_id__exact=question_id, course_id=course_id)

    tmpJson = serializers.serialize("json", allVote)
    tmpObj = json.loads(tmpJson)

    return JsonResponse({'alldata': tmpObj})


def homepage(request):
    return render(
        request,
        'index.html',
        {
            'title': 'Homepage',
        }
    )


def vote(request):
    try:
        getid = request.GET['id_data']
    except MultiValueDictKeyError:
        getid = False

    current_user = request.user
    if current_user.is_authenticated:

        if getid is False:
            try:
                question = Question.objects.order_by('id').first()

            except Question.DoesNotExist:
                question = None

            if question is not None:
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
                vote_values = Vote.objects.filter(question_id__exact=question_id).filter(user_id=current_user.id).first()
                if vote_values is None:
                    vote_comment = ""
                else:
                    vote_comment = vote_values.comment_data

            except Vote.DoesNotExist:
                vote_value = None

            try:
                usercourse = UserCourse.objects.get(user__exact=current_user.id)
                course_id = usercourse.course_id
                course = Course.objects.get(id=course_id)
            except UserCourse.DoesNotExist:
                course_id = 0

            try:
                votes = Vote.objects.filter(question_id=question_id, course_id=course_id)
                vote_count = votes.count()
            except Vote.DoesNotExist:
                vote_count = 0

            if course.status is not None:
                if course.status == 0:
                    vote_value = vote_values.value
                elif course.status == 1:
                    vote_value = vote_values.revised_value

        else:
            questiondata = None
            next_issue = None
            last_issue = None
            left_hints = None
            middle_hints = None
            right_hints = None
            vote_count = None
            vote_value = None
            course_id = None

        return render(
            request,
            'members/vote.html',
            {
                'question': questiondata,
                'question_id': question_id,
                'next_id': next_issue,
                'back_id': last_issue,
                'left_hints':  left_hints,
                'middle_hints': middle_hints,
                'right_hints': right_hints,
                'course_id': course_id,
                'vote_value': vote_value,
                'vote_count': vote_count,
                'course_status': course.status,
                'vote_comment': vote_comment,
                'original_vote_value': vote_values.value
            }
        )

    else:
        return redirect(reverse('login'))








