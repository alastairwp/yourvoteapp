from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from domain_admin.models import UserCentre
from btbadmin.models import Centre
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from send_email.views import send_email
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.urls import reverse
from pullingapp import settings


def register(request):

    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        centre = request.POST['centre']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Username already taken')
                return redirect(reverse('register'))
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already taken')
                return redirect(reverse('register'))
            else:
                # Create new user
                user = User.objects.create_user(username=email, email=email, password=password1, first_name=first_name, last_name=last_name, is_active=False)
                user.save()

                #  Assign user to a centre
                user_centre = UserCentre(user_id=user.id, centre_id=centre)
                user_centre.save()

                # Add user to default groups
                members_group = Group.objects.get(name='members')
                none_group = Group.objects.get(name="none")
                user.groups.add(members_group)
                user.groups.add(none_group)

                current_site = get_current_site(request)

                if settings.EMAIL_USE_TLS is True:
                    hypertext = "https://"
                else:
                    hypertext = "http://"

                ctx = {}
                ctx["first_name"] = first_name
                ctx["activation_uid"] = urlsafe_base64_encode(force_bytes(user.pk))
                ctx["activation_token"] = account_activation_token.make_token(user)
                ctx["domain"] = hypertext + current_site.domain

                emails = (email,)
                send_email(request, "activation_email", ctx, emails)

                messages.success(request, "Account created successfully. Check your email inbox for a verification email.")
                return redirect(reverse('login'))
        else:
            messages.warning(request, 'Passwords do not match')
            return redirect(reverse('register'))

    centres = Centre.objects.all()

    return render(
        request, 'register.html',
        {
            'centres': centres,
            'active_tab': "home"
        }
    )


def activate(request, uidb64, token):
    message = ""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        message = "Thank you for your email confirmation. Now you can login your account."

    else:
        message = "Activation link is invalid!"

    return render(
        request, 'email_activation.html',
        {
            'message': message
        }
    )
