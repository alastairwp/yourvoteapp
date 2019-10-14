from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth
from django.urls import reverse


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth.login(request, user)
                return redirect(reverse('dashboard'))

            else:
                messages.warning(request,
                                 "Your account is not active. If you've just registered check your inbox for an activation email. Alternatively contact support.")
                return redirect(reverse('login'))

        else:
            messages.error(request, 'Invalid username/password')
            return redirect(reverse('login'))
    else:
        return render(request, 'login.html')




