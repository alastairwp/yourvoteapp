from django.db import models


class EmailTemplate(models.Model):
    name = models.CharField("Template Name", max_length=255, null=False, blank=False)
    sender = models.CharField("Sender", max_length=255, null=False, blank=False)
    reply_to = models.CharField("Reply-To", max_length=255, null=False, blank=False)
    subject_line_template = models.CharField("Subject", max_length=255, null=False, blank=False)
    plain_text_template = models.TextField("Plain text template", null=False, blank=False)
    html_template = models.TextField("HTML template", null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

