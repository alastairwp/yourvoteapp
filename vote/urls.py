from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.vote, name='vote'),
    path('save_vote_data', views.save_vote_data, name='save_vote'),
    path('vote/get_chart_data', views.get_chart_data, name='get_chart_data')
]
