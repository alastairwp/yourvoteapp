from django.shortcuts import render
from django.core.mail import send_mail
from .models import EmailTemplate
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email(request):
    invite_template = EmailTemplate.objects.get(name='invite_participant')
    html_content_template = invite_template.html_template
    html_content = render_to_string(html_content_template, {'first_name': 'Donald'})
    email = EmailMessage(invite_template.subject_line_template, html_content, invite_template.sender, ['awp@yugen.digital'])
    email.content_subtype = "html"
    res = email.send()

