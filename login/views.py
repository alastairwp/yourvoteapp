from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/members/dashboard')
        else:
            messages.info(request, 'Your username or password is incorrect')
            return redirect('/login')
    else:
        return render(request, 'login.html')




