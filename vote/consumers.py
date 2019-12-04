from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Count
from domain_admin.models import Course, UserCourse
from django.utils import timezone
from .models import Vote
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['question_id']
        self.room_group_name = 'vote_%s' % self.room_name
        self.user = self.scope['user']

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        vote = text_data_json['vote']
        course_id = text_data_json['course']
        question_id = text_data_json['question']
        comment_data = text_data_json['comment']
        current_user = self.scope['user']
        now = timezone.now()

        course = Course.objects.get(id=course_id)
        if vote != 0:

            # Check to see if user has voted on this question already
            try:
                checkvote = Vote.objects.filter(user__exact=current_user.id, question_id__exact=question_id,
                                                course_id=course_id).count()
            except Vote.DoesNotExist:
                checkvote = 0

            # If the user has voted...
            if checkvote != 0:
                checkvote = Vote.objects.get(user__exact=current_user.id, question_id__exact=question_id,
                                             course_id=course_id)

                # check if course is in first or second stage and saved the value
                if course.status == 0:
                    Vote.objects.filter(id=checkvote.id).update(comment_data=comment_data, value=vote, course_id=course_id, updated_date=now)

                elif course.status == 1:
                    Vote.objects.filter(id=checkvote.id).update(comment_data=comment_data, revised_value=vote,
                                                                course_id=course_id, updated_date=now)

            # User hasn't voted on this question before so created a new vote record
            else:
                if course.status == 0:
                    savequestion = Vote(user=current_user, question_id=question_id, value=vote, comment_data=comment_data, course_id=course_id, updated_date=now)
                    savequestion.save()

                elif course.status == 1:
                    savequestion = Vote(user=current_user, question_id=question_id, revised_value=vote, comment_data=comment_data,
                                        course_id=course_id, updated_date=now)
                    savequestion.save()
        try:
            if course.status == 0:
                votes = Vote.objects.values('value').order_by('value').annotate(count=Count('value')).filter(
                    course_id=course_id).filter(question_id=question_id)
                vote_count = votes.count()
                all_votes = Vote.objects.filter(question_id=question_id, course_id=course_id, value__gt=0)
                votes_by_userid = Vote.objects.filter(question_id=question_id, course_id=course_id, value__gt=0).values(
                    'user_id')
                users_yet_to_vote = UserCourse.objects.filter(course_id=course_id).exclude(user_id__in=votes_by_userid)
                not_voted_users = []
                voted_users = []
                for unvote in users_yet_to_vote:
                    if not unvote.user.groups.filter(name__in=['domain_admins', 'presenters', 'btbadmins']).exists():
                        not_voted_users.append(
                            "<div style='float:left;margin-top:10px;border-radius:5px;margin-left:10px;color:white;display:inline;border:1px solid green;padding:5px;background-color:#23527c'>" + unvote.user.first_name + ' ' + unvote.user.last_name + "</div>")

                for uvote in all_votes:
                    voted_users.append(
                        "<div style='float:left;margin-top:10px;border-radius:5px;margin-left:10px;color:white;display:inline;border:1px solid green;padding:5px;background-color:#009900'>" + uvote.user.first_name + ' ' + uvote.user.last_name + "</div>")
        except Vote.DoesNotExist:
            vote_count = 0

        try:
            if course.status > 0:
                votes = Vote.objects.values('revised_value').order_by('revised_value').annotate(
                    count=Count('revised_value')).filter(
                    course_id=course_id).filter(question_id=question_id)
                vote_count = votes.count()
                all_votes = Vote.objects.filter(question_id=question_id, course_id=course_id, revised_value__gt=0)
                votes_by_userid = Vote.objects.filter(question_id=question_id, course_id=course_id,
                                                      revised_value__gt=0).values('user_id')
                users_yet_to_vote = UserCourse.objects.filter(course_id=course_id).exclude(user_id__in=votes_by_userid)
                not_voted_users = []
                voted_users = []
                for unvote in users_yet_to_vote:
                    if not unvote.user.groups.filter(name__in=['domain_admins', 'presenters', 'btbadmins']).exists():
                        not_voted_users.append(
                            "<div style='float:left;margin-top:10px;border-radius:5px;margin-left:10px;color:white;display:inline;border:1px solid green;padding:5px;background-color:#23527c'>" + unvote.user.first_name + ' ' + unvote.user.last_name + "</div>")

                for uvote in all_votes:
                    voted_users.append(
                        "<div style='float:left;margin-top:10px;border-radius:5px;margin-left:10px;color:white;display:inline;border:1px solid green;padding:5px;background-color:#009900'>" + uvote.user.first_name + ' ' + uvote.user.last_name + "</div>")

        except Vote.DoesNotExist:
            vote_count = 0

        allvotes = []
        for x in range(1, 10):
            trigger = False
            for vote_item in votes:
                if course.status == 0:
                    if int(vote_item['value']) == x:
                        allvotes.append(vote_item['count'])
                        trigger = True
                        break
                else:
                    if int(vote_item['revised_value']) == x:
                        allvotes.append(vote_item['count'])
                        trigger = True
                        break
            if trigger is False:
                allvotes.append(0)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'vote': vote,
                'allvotes': allvotes,
                'vote_count': vote_count,
                'voted_users': voted_users,
                'not_voted_users': not_voted_users,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        vote = event['vote']
        allvotes = event['allvotes']
        vote_count = event['vote_count']
        voted_users = event['voted_users']
        not_voted_users = event['not_voted_users']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'vote': vote,
            'allvotes': allvotes,
            'vote_count': vote_count,
            'voted_users': voted_users,
            'not_voted_users': not_voted_users,
        }))