from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def dashboard(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'members/dashboard.html',
        {

        }
    )