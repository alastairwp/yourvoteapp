from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'^ws/members/vote/(?P<question_id>\d+)/$', consumers.ChatConsumer),
]