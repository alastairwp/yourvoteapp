from django.db import models
from django.contrib.auth.models import Group


class Centre(models.Model):
    name = models.CharField("Centre name", max_length=100, null=False, blank=False)
    admin_user_group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)

