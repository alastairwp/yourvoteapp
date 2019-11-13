from django.db import models


class UserDataCapture(models.Model):
    email = models.CharField("Email", max_length=255, null=False, blank=False)
    first_name = models.CharField("First name", max_length=255, null=False, blank=False)
    last_name = models.CharField("Last name", max_length=255, null=False, blank=False)
    gdpr_opt_in = models.BooleanField("GDPR Opt-in", default=False)
    created_date = models.DateTimeField(auto_now_add=True)
