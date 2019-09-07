from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.benchmark, name='benchmark'),
    path('save_vote_data', views.save_vote_data, name='save_vote'),
    path('benchmark/get_chart_data', views.get_chart_data, name='get_chart_data')
]
