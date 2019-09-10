from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages

def register(request):

    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Username already taken')
                return redirect('/register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('/register')
            else:
                user = User.objects.create_user(username=email, email=email, password=password1, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, 'User Created')
                return redirect('/login')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('/register')

    else:
        return render(request, 'register.html')