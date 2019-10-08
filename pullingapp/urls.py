"""pullingapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.vote, name='vote')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='vote')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.urls import path, re_path
from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.auth.views as auth_views
import vote.views as vote_views
import login.views
import domain_admin.views as domain_admin_views
import btbadmin.views as btbadmin_views
import send_email.views as send_email_views
import register.views as register_views
import vote.views as vote_views

urlpatterns = [
    path('', vote_views.homepage, name='homepage'),
    re_path(r'^.well-known/acme-challenge/-2HCzvSJ-_aPSu1tt7ktUKcSHGw37YN8NRsMTUVJJyM$', vote_views.acme_challenge, name='acme-challenge'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', register_views.activate, name='activate'),
    path('sendmail/', send_email_views.send_email),
    path('save_vote_data', vote_views.save_vote_data),
    path('save_comment_data', vote_views.save_comment_data),
    path('get_chart_data', vote_views.get_chart_data),
    path('register', include('register.urls')),
    path('login', login.views.login, name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('members/', include('members.urls')),
    path('domain_admin', domain_admin_views.domain_admin_home, name='domain_admin_home'),
    re_path(r'^domain_admin/course/(?P<course_id>\d+)$', domain_admin_views.edit_course, name='centre_admin_edit_course'),
    re_path(r'^btbadmin/centre/(?P<centre_id>\d+)$', btbadmin_views.edit_centre, name='edit_centre'),
    re_path(r'^btbadmin/course/(?P<course_id>\d+)$', btbadmin_views.edit_course, name='admin_edit_course'),
    re_path(r'^btbadmin/user/(?P<user_id>\d+)$', btbadmin_views.edit_user, name='edit_centre'),
    path('btbadmin', btbadmin_views.btbadmin_home, name='btbadmin_home'),
    path('admin/', admin.site.urls),
]
