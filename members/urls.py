from django.urls import path, re_path
from . import views
import vote.views as vote_views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    re_path(r'^account/(?P<user_id>\d+)/$', views.account_profile, name="account-profile"),
    re_path(r'^course/(?P<course_code>\w+)/$', views.course_home, name='course_home'),
    path('vote/', vote_views.vote, name='vote'),
    re_path(r'^assessment-report/(?P<course_id>\d+)/$', views.assessmentreport, name='course-report'),
    path('password_change/', PasswordChangeView.as_view(template_name='members/password_change_form.html')),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='members/password_change_done.html')),
    path('password_reset/', PasswordResetView.as_view(template_name='members/password_reset_form.html'), {'is_secure': True}),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='members/password_reset_done.html'), name="password_reset_done"),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            PasswordResetConfirmView.as_view(template_name='members/password_reset_confirm.html'), name="password_reset_confirm"),
    path('reset_done/', PasswordResetCompleteView.as_view(template_name='members/password_reset_complete.html'), name="password_reset_complete"),

]
