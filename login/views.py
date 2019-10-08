from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth.login(request, user)
                return redirect('/members/dashboard')

            else:
                messages.warning(request,
                                 "Your account is not active. If you've just registered check your inbox for an activation email. Alternatively contact support.")
                return redirect('/login')

        else:
            messages.error(request, 'Invalid username/password')
            return redirect('/login')
    else:
        return render(request, 'login.html')




