from django.contrib import admin
from .models import UserDataCapture


class UserDataCaptureAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name", "gdpr_opt_in"]

    class Meta:
        Model = UserDataCapture


admin.site.register(UserDataCapture, UserDataCaptureAdmin)
