from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Question, Vote, Hint
from domain_admin.models import UserCourse, Course
from btbadmin.models import Centre
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone
from django.core import serializers
import json
from django import template
from django.urls import reverse


register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


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
        comment_data = comment_data.replace("'", "''")
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

    try:
        course_status = request.POST['course_status']
    except MultiValueDictKeyError:
        course_status = 0

    try:
        if int(course_status) == 0:
            votes_by_userid = Vote.objects.filter(question_id=question_id, course_id=course_id, value__gt=0).values('user_id')
            votes = Vote.objects.filter(question_id=question_id, course_id=course_id, value__gt=0)
            users_yet_to_vote = UserCourse.objects.filter(course_id=course_id).exclude(user_id__in=votes_by_userid)
            vote_count = votes.count()
            not_voted_users = []
            voted_users = []
            for unvote in users_yet_to_vote:
                if not unvote.user.groups.filter(name__in=['domain_admins', 'presenters', 'btbadmins']).exists():
                    not_voted_users.append("<div style='float:left;margin-top:10px;border-radius:5px;margin-left:10px;color:white;display:inline;border:1px solid green;padding:5px;background-color:#23527c'>" + unvote.user.first_name + ' ' + unvote.user.last_name + "</div>")

            for uvote in votes:
                voted_users.append("<div style='float:left;margin-top:10px;border-radius:5px;margin-left:10px;color:white;display:inline;border:1px solid green;padding:5px;background-color:#009900'>" + uvote.user.first_name + ' ' + uvote.user.last_name + "</div>")
    except Vote.DoesNotExist:
        vote_count = 0

    try:
        if int(course_status) > 0:
            revised_votes = Vote.objects.filter(question_id=question_id, course_id=course_id, revised_value__gt=0)
            vote_count = revised_votes.count()
            voted_users = []
            for uvote in revised_votes:
                voted_users.append("<div style='float:left;margin-top:10px;border-radius:5px;margin-left:10px;color:white;display:inline;border:1px solid green;padding:5px;background-color:#009900'>" + uvote.user.first_name + ' ' + uvote.user.last_name + "</div>")
    except Vote.DoesNotExist:
        vote_count = 0

    allVote = Vote.objects.filter(question_id__exact=question_id, course_id=course_id)
    tmpJson = serializers.serialize("json", allVote)
    tmpObj = json.loads(tmpJson)

    return JsonResponse({'alldata': tmpObj, 'vote_count': vote_count, 'voted_users': voted_users, 'not_voted_users': not_voted_users})


def homepage(request):
    centres = Centre.objects.all()
    return render(
        request,
        'index.html',
        {
            'title': 'Homepage',
            'centres': centres
        }
    )


def cookiepolicy(request):
    return render(
        request,
        'cookiepolicy.html',
        {
            'title': 'Cookie Policy'
        }
    )


def website_terms(request):
    return render(
        request,
        'website-terms.html',
        {
            'title': 'Terms & Conditions'
        }
    )


def privacy_policy(request):
    return render(
        request,
        'privacy-policy.html',
        {
            'title': 'Privacy Policy'
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
                vote_values = Vote.objects.filter(question_id__exact=question_id).filter(user_id=current_user.id).order_by('-created_date')[:1].get()
            except Vote.DoesNotExist:
                vote_values = None

            if vote_values is None:
                vote_comment = ""
            else:
                vote_comment = vote_values.comment_data
                vote_comment = vote_comment.replace("''", "'")
                
            try:
                usercourse = UserCourse.objects.get(user__exact=current_user.id)
                course_id = usercourse.course_id
                course = Course.objects.get(id=course_id)
            except UserCourse.DoesNotExist:
                course_id = 0

            try:
                if course.status == 0:
                    votes = Vote.objects.filter(question_id=question_id, course_id=course_id, value__gt=0)
                    vote_count = votes.count()
            except Vote.DoesNotExist:
                vote_count = 0

            try:
                if course.status > 0:
                    revised_votes = Vote.objects.filter(question_id=question_id, course_id=course_id, revised_value__gt=0)
                    vote_count = revised_votes.count()
            except Vote.DoesNotExist:
                vote_count = 0

            #  get number of questions answered
            try:
                if int(course.status) == 0:
                    questions_answered = Vote.objects.filter(user_id=current_user.id, course_id=course_id).exclude(value=0)
                    question_count = questions_answered.count()
            except Vote.DoesNotExist:
                question_count = 0

            if course.status is not None:
                if course.status == 0:
                    if vote_values:
                        vote_value = vote_values.value
                    else:
                        vote_value = 0
                elif course.status == 1:
                    if vote_values:
                        vote_value = vote_values.revised_value
                    else:
                        vote_value = 0

            if vote_values is None:
                original_vote_value = 0
            else:
                original_vote_value = vote_values.value

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
            vote_comment = ""

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
                'original_vote_value': original_vote_value,
                'question_count': question_count,
            }
        )

    else:
        return redirect(reverse('login'))








