from django.urls import path, re_path
from django.conf.urls import include
from django.contrib import admin
import django.contrib.auth.views as auth_views
import login.views
import domain_admin.views as domain_admin_views
import btbadmin.views as btbadmin_views
import send_email.views as send_email_views
import register.views as register_views
import vote.views as vote_views
import members.views as members_views


handler404 = 'members.views.handler404'
handler500 = 'members.views.handler500'

urlpatterns = [
    path('404/', members_views.handler404, name='404'),
    path('', vote_views.homepage, name='homepage'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', register_views.activate, name='activate'),
    path('sendmail/', send_email_views.send_email),
    path('save_vote_data/', vote_views.save_vote_data),
    path('save_comment_data/', vote_views.save_comment_data),
    path('get_chart_data', vote_views.get_chart_data),
    path('register/', include('register.urls')),
    path('login/', login.views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('members/', include('members.urls')),
    path('cookie-policy/', vote_views.cookiepolicy, name='cookie_policy'),
    path('website-terms/', vote_views.website_terms, name='website_terms'),
    path('privacy-policy/', vote_views.privacy_policy, name='privacy_policy'),
    path('domain_admin/', domain_admin_views.domain_admin_home, name='domain_admin_home'),
    re_path(r'^domain_admin/course/(?P<course_id>\d+)/$', domain_admin_views.edit_course, name='centre_admin_edit_course'),
    re_path(r'^btbadmin/centre/(?P<centre_id>\d+)/$', btbadmin_views.edit_centre, name='edit_centre'),
    re_path(r'^btbadmin/course/(?P<course_id>\d+)/$', btbadmin_views.edit_course, name='admin_edit_course'),
    re_path(r'^btbadmin/user/(?P<user_id>\d+)/$', btbadmin_views.edit_user, name='edit_user'),
    path('btbadmin/', btbadmin_views.btbadmin_home, name='btbadmin_home'),
    path('admin/', admin.site.urls),
]

