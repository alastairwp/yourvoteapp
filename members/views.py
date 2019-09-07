from django.shortcuts import render
from benchmark.models import UserCourse


def dashboard(request):
    current_user = request.user
    courses = UserCourse.objects.filter(user=current_user.id)
    return render(
        request,
        'members/dashboard.html',
        {
            'title': 'PtP Dashboard',
            'courses': courses
        }
    )
