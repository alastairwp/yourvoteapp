from django.shortcuts import render
from django.core.mail import send_mail
from .models import EmailTemplate
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import redirect


def send_email(request, template, ctx, to_emails):
    send_email_result = EmailTemplate.send(template, ctx, emails=to_emails)


