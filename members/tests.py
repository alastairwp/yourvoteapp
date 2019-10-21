from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import dashboard, course_home, assessmentreport
from vote.views import vote


class TestMembersUrls(SimpleTestCase):

    def test_dashboard_url_resolves(self):
        url = reverse('dashboard')
        self.assertEquals(resolve(url).func, dashboard)

    def test_course_home_url_resolves(self):
        url = reverse('course_home', args=["PTPBTM001"])
        self.assertEquals(resolve(url).func, course_home)

    def test_vote_url_resolves(self):
        url = reverse('vote')
        self.assertEquals(resolve(url).func, vote)

    def test_course_report_url_resolves(self):
        url = reverse('course-report', args=["1"])
        self.assertEquals(resolve(url).func, assessmentreport)
