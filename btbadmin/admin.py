from django.contrib import admin
from .models import Centre


class CentreAdmin(admin.ModelAdmin):
    list_display = ["name"]

    class Meta:
        Model = Centre


admin.site.register(Centre, CentreAdmin)
