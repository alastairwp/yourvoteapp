from django.contrib import admin
from .models import EmailTemplate


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "sender", "reply_to", "subject_line_template"]

    class Meta:
        Model = EmailTemplate


admin.site.register(EmailTemplate, EmailTemplateAdmin)
